import json
from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.opportunity import Opportunity


def _row(item: Opportunity):
    return {
        "id": item.id,
        "title": item.title,
        "company": item.company_name,
        "industry": item.industry,
        "province": item.province,
        "city": item.city,
        "type": item.opportunity_type,
        "score": item.total_score,
        "urgency": item.urgency_score,
        "confidence": item.confidence_score,
        "status": item.status,
        "summary": item.summary,
        "bearing_types": item.bearing_types,
        "bearing_models": item.bearing_models,
        "equipment_types": item.equipment_types,
        "recommended_action": item.recommended_action,
        "confidence_reason": item.confidence_reason,
    }


def get_visible_opportunities(db: Session, limit: int = 20):
    return (
        db.query(Opportunity)
        .filter(Opportunity.status != "invalid")
        .order_by(Opportunity.total_score.desc(), Opportunity.updated_at.desc())
        .limit(limit)
        .all()
    )


def build_context(items) -> str:
    return json.dumps([_row(item) for item in items], ensure_ascii=False, indent=2)


def fallback_answer(question: str, items) -> str:
    q = question.lower()
    selected = items
    if "steel" in q or "钢" in question:
        selected = [x for x in selected if x.industry == "钢铁"]
    if "chemical" in q or "化工" in question:
        selected = [x for x in selected if x.industry == "化工"]
    if "high" in q or "priority" in q or "top" in q or "最高" in question:
        selected = sorted(selected, key=lambda x: x.total_score, reverse=True)[:5]

    if not selected:
        selected = items[:5]

    lines = [
        "I can answer from the current opportunity database. LLM credentials are not configured yet, so this is a deterministic database summary.",
        "",
        f"Visible opportunities: {len(items)}.",
        "Top matching items:",
    ]
    for item in selected[:6]:
        lines.append(
            f"- #{item.id} {item.title} | company: {item.company_name or '-'} | "
            f"industry: {item.industry or '-'} | score: {item.total_score} | "
            f"urgency: {item.urgency_score} | confidence: {item.confidence_score}."
        )
        if item.recommended_action:
            lines.append(f"  Recommended action: {item.recommended_action}")
    return "\n".join(lines)


async def llm_answer(question: str, items):
    if not settings.llm_base_url or not settings.llm_api_key or not settings.llm_model:
        return None

    context = build_context(items)
    system = (
        "You are a bearing sales opportunity analyst. Answer in English. "
        "Use only the provided database context. If data is missing, say what needs verification. "
        "Be concise, cite opportunity IDs, and provide sales follow-up actions."
    )
    user = f"Question:\n{question}\n\nOpportunity database context:\n{context}"

    base = settings.llm_base_url.rstrip("/")
    url = f"{base}/chat/completions"
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
    }
    headers = {"Authorization": f"Bearer {settings.llm_api_key}", "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    return data["choices"][0]["message"]["content"]


async def answer_question(db: Session, question: str):
    items = get_visible_opportunities(db)
    try:
        answer = await llm_answer(question, items)
        if answer:
            return answer, "llm"
    except Exception as exc:
        text = str(exc)
        if "429" in text or "Too Many Requests" in text:
            note = "LLM is configured with the doc2graph model, but the provider is currently rate-limited. Using database fallback for this answer."
            return fallback_answer(question, items) + f"\n\n{note}", "fallback_rate_limited"
        note = "LLM is configured but the call failed. Using database fallback for this answer."
        return fallback_answer(question, items) + f"\n\n{note}", "fallback_after_llm_error"

    return fallback_answer(question, items), "fallback_no_llm_key"
