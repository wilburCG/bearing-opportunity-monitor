"""Import real opportunity records from a JSON file.

Usage:
  docker compose exec -T backend python -m app.scripts.import_opportunities_json /app/data/real_opportunities.json

JSON shape: list[dict] with source_url plus Opportunity fields.
"""
import asyncio
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from app.db.session import SessionLocal
from app.models.opportunity import Opportunity
from app.models.opportunity_source import OpportunitySource
from app.models.source import Source
from app.services.geocoding import geocode_opportunity_location
from app.services.scoring import compute_fit_score, compute_total_score


def parse_dt(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace('Z', '+00:00')).replace(tzinfo=None)
    except ValueError:
        # Try simple YYYY-MM-DD.
        try:
            return datetime.strptime(text[:10], '%Y-%m-%d')
        except ValueError:
            return None


def normalize_items(value):
    if value is None:
        return None
    if isinstance(value, dict):
        items = value.get('items') or []
    elif isinstance(value, list):
        items = value
    elif isinstance(value, str) and value.strip():
        items = [x.strip() for x in value.replace('，', ',').split(',') if x.strip()]
    else:
        items = []
    return {'items': [str(x).strip() for x in items if str(x).strip()]}


def clean_score(value, default=50):
    try:
        score = float(value)
    except (TypeError, ValueError):
        return default
    return max(0, min(100, score))


def text_hash(text):
    if not text:
        return None
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def geocode_sync(raw: dict[str, Any]):
    return asyncio.run(geocode_opportunity_location(
        province=raw.get('province'),
        city=raw.get('city'),
        district=raw.get('district'),
        address=raw.get('address'),
        company_name=raw.get('company_name'),
        title=raw.get('title'),
    ))


def main(path: str):
    payload = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(payload, list):
        raise SystemExit('JSON root must be a list')

    def apply_if_present(obj, attr, value, transform=None, max_len=None):
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if transform:
            value = transform(value)
        if max_len and isinstance(value, str):
            value = value[:max_len]
        if getattr(obj, attr) != value:
            setattr(obj, attr, value)
            return True
        return False

    def find_existing_opportunity(title: str, company_name: str | None):
        query = db.query(Opportunity).filter(Opportunity.title == title[:512])
        if company_name:
            match = query.filter(Opportunity.company_name == company_name).first()
            if match:
                return match
        return query.first()

    db = SessionLocal()
    created = 0
    updated = 0
    linked = 0
    skipped = 0
    try:
        for raw in payload:
            source_url = (raw.get('source_url') or raw.get('url') or '').strip()
            title = (raw.get('title') or '').strip()
            if not source_url or not title:
                skipped += 1
                continue

            industry = raw.get('industry')
            volume_score = clean_score(raw.get('volume_score'), 50)
            urgency_score = clean_score(raw.get('urgency_score'), 50)
            confidence_score = clean_score(raw.get('confidence_score'), 50)
            fit_score = clean_score(raw.get('fit_score'), compute_fit_score(industry))
            total_score = clean_score(raw.get('total_score'), compute_total_score(volume_score, urgency_score, confidence_score, fit_score))
            content_text = raw.get('content_text') or raw.get('evidence_snippet') or raw.get('summary')

            source = db.query(Source).filter(Source.url == source_url[:512]).first()
            opportunity = None
            if source:
                link = db.query(OpportunitySource).filter(OpportunitySource.source_id == source.id).first()
                if link:
                    opportunity = db.get(Opportunity, link.opportunity_id)

            if not opportunity:
                opportunity = find_existing_opportunity(title, raw.get('company_name'))

            if opportunity:
                changed = False
                for attr, value, max_len in [
                    ('summary', raw.get('summary'), None),
                    ('opportunity_type', raw.get('opportunity_type'), 64),
                    ('industry', industry, 64),
                    ('company_name', raw.get('company_name'), 256),
                    ('project_name', raw.get('project_name'), 256),
                    ('province', raw.get('province'), 64),
                    ('city', raw.get('city'), 64),
                    ('district', raw.get('district'), 64),
                    ('address', raw.get('address'), 512),
                    ('estimated_quantity', raw.get('estimated_quantity'), 128),
                    ('estimated_amount', raw.get('estimated_amount'), 128),
                    ('confidence_reason', raw.get('confidence_reason'), None),
                    ('recommended_action', raw.get('recommended_action'), None),
                ]:
                    changed |= apply_if_present(opportunity, attr, value, max_len=max_len)
                changed |= apply_if_present(opportunity, 'latitude', raw.get('latitude'))
                changed |= apply_if_present(opportunity, 'longitude', raw.get('longitude'))
                if opportunity.latitude is None or opportunity.longitude is None:
                    geocoded = geocode_sync({**raw, 'title': title})
                    if geocoded:
                        changed |= apply_if_present(opportunity, 'latitude', geocoded.latitude)
                        changed |= apply_if_present(opportunity, 'longitude', geocoded.longitude)
                changed |= apply_if_present(opportunity, 'deadline_at', raw.get('deadline_at'), transform=parse_dt)
                changed |= apply_if_present(opportunity, 'bearing_types', raw.get('bearing_types'), transform=normalize_items)
                changed |= apply_if_present(opportunity, 'bearing_models', raw.get('bearing_models'), transform=normalize_items)
                changed |= apply_if_present(opportunity, 'equipment_types', raw.get('equipment_types'), transform=normalize_items)
                for attr, value in [
                    ('volume_score', volume_score),
                    ('urgency_score', urgency_score),
                    ('confidence_score', confidence_score),
                    ('fit_score', fit_score),
                    ('total_score', total_score),
                ]:
                    changed |= apply_if_present(opportunity, attr, value)
                if opportunity.status == 'invalid':
                    opportunity.status = 'new'
                    changed = True
                if changed:
                    opportunity.updated_at = datetime.utcnow()
                    updated += 1
            else:
                latitude = raw.get('latitude')
                longitude = raw.get('longitude')
                if latitude is None or longitude is None:
                    geocoded = geocode_sync({**raw, 'title': title})
                    if geocoded:
                        latitude = geocoded.latitude
                        longitude = geocoded.longitude
                opportunity = Opportunity(
                    title=title[:512],
                    summary=raw.get('summary'),
                    opportunity_type=raw.get('opportunity_type'),
                    industry=industry,
                    company_name=raw.get('company_name'),
                    project_name=raw.get('project_name'),
                    province=raw.get('province'),
                    city=raw.get('city'),
                    district=raw.get('district'),
                    address=raw.get('address'),
                    latitude=latitude,
                    longitude=longitude,
                    bearing_types=normalize_items(raw.get('bearing_types')),
                    bearing_models=normalize_items(raw.get('bearing_models')),
                    equipment_types=normalize_items(raw.get('equipment_types')),
                    estimated_quantity=raw.get('estimated_quantity'),
                    estimated_amount=raw.get('estimated_amount'),
                    deadline_at=parse_dt(raw.get('deadline_at')),
                    volume_score=volume_score,
                    urgency_score=urgency_score,
                    confidence_score=confidence_score,
                    fit_score=fit_score,
                    total_score=total_score,
                    confidence_reason=raw.get('confidence_reason'),
                    recommended_action=raw.get('recommended_action'),
                    status='new',
                )
                db.add(opportunity)
                db.flush()
                created += 1

            if source:
                source_changed = False
                source_changed |= apply_if_present(source, 'title', raw.get('source_title') or title, max_len=512)
                source_changed |= apply_if_present(source, 'source_site', raw.get('source_site'), max_len=128)
                source_changed |= apply_if_present(source, 'source_type', raw.get('source_type') or raw.get('opportunity_type'), max_len=64)
                source_changed |= apply_if_present(source, 'published_at', raw.get('published_at'), transform=parse_dt)
                source_changed |= apply_if_present(source, 'raw_text_hash', text_hash(content_text), max_len=64)
                source_changed |= apply_if_present(source, 'content_text', content_text)
                source_changed |= apply_if_present(source, 'content_summary', raw.get('summary'))
                source_changed |= apply_if_present(source, 'credibility_level', raw.get('credibility_level'), max_len=32)
                if source_changed:
                    source.fetched_at = datetime.utcnow()
            else:
                source = Source(
                    url=source_url[:512],
                    title=(raw.get('source_title') or title)[:512],
                    source_site=raw.get('source_site'),
                    source_type=raw.get('source_type') or raw.get('opportunity_type'),
                    published_at=parse_dt(raw.get('published_at')),
                    raw_text_hash=text_hash(content_text),
                    content_text=content_text,
                    content_summary=raw.get('summary'),
                    credibility_level=raw.get('credibility_level'),
                )
                db.add(source)
                db.flush()

            link = db.query(OpportunitySource).filter(
                OpportunitySource.opportunity_id == opportunity.id,
                OpportunitySource.source_id == source.id,
            ).first()
            if link:
                apply_if_present(link, 'evidence_snippet', raw.get('evidence_snippet'))
                apply_if_present(link, 'extraction_confidence', confidence_score)
            else:
                db.add(OpportunitySource(
                    opportunity_id=opportunity.id,
                    source_id=source.id,
                    evidence_snippet=raw.get('evidence_snippet'),
                    extraction_confidence=confidence_score,
                ))
                linked += 1

        db.commit()
        print(json.dumps({'created': created, 'updated': updated, 'linked': linked, 'skipped': skipped}, ensure_ascii=False))
    finally:
        db.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python -m app.scripts.import_opportunities_json <path>')
    main(sys.argv[1])
