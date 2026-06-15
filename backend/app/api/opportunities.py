from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.opportunity import Opportunity
from app.schemas.opportunity import OpportunityOut, OpportunityDetailOut, OpportunityStatusUpdate

router = APIRouter()


@router.get("", response_model=list[OpportunityOut])
def list_opportunities(
    industry: str | None = None,
    province: str | None = None,
    opportunity_type: str | None = None,
    status: str | None = None,
    min_score: float | None = None,
    max_score: float | None = None,
    min_urgency: float | None = None,
    max_urgency: float | None = None,
    min_confidence: float | None = None,
    max_confidence: float | None = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(Opportunity)
    if industry:
        query = query.filter(Opportunity.industry == industry)
    if province:
        query = query.filter(Opportunity.province == province)
    if opportunity_type:
        query = query.filter(Opportunity.opportunity_type == opportunity_type)
    if status:
        query = query.filter(Opportunity.status == status)
    else:
        query = query.filter(Opportunity.status != "invalid")
    if min_score is not None:
        query = query.filter(Opportunity.total_score >= min_score)
    if max_score is not None:
        query = query.filter(Opportunity.total_score <= max_score)
    if min_urgency is not None:
        query = query.filter(Opportunity.urgency_score >= min_urgency)
    if max_urgency is not None:
        query = query.filter(Opportunity.urgency_score <= max_urgency)
    if min_confidence is not None:
        query = query.filter(Opportunity.confidence_score >= min_confidence)
    if max_confidence is not None:
        query = query.filter(Opportunity.confidence_score <= max_confidence)
    return query.order_by(Opportunity.total_score.desc(), Opportunity.updated_at.desc()).limit(limit).all()


@router.get("/{opportunity_id}", response_model=OpportunityDetailOut)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    item = db.get(Opportunity, opportunity_id)
    if not item:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return item


@router.patch("/{opportunity_id}/status", response_model=OpportunityDetailOut)
def update_status(opportunity_id: int, payload: OpportunityStatusUpdate, db: Session = Depends(get_db)):
    item = db.get(Opportunity, opportunity_id)
    if not item:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    item.status = payload.status
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
