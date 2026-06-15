from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.opportunity import Opportunity
from app.models.opportunity_note import OpportunityNote

router = APIRouter()


class OpportunityNoteCreate(BaseModel):
    note: str
    operator: str | None = None


class OpportunityNoteOut(BaseModel):
    id: int
    opportunity_id: int
    note: str
    operator: str | None = None

    class Config:
        from_attributes = True


@router.get("/{opportunity_id}/notes", response_model=list[OpportunityNoteOut])
def list_notes(opportunity_id: int, db: Session = Depends(get_db)):
    if not db.get(Opportunity, opportunity_id):
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return (
        db.query(OpportunityNote)
        .filter(OpportunityNote.opportunity_id == opportunity_id)
        .order_by(OpportunityNote.created_at.desc())
        .all()
    )


@router.post("/{opportunity_id}/notes", response_model=OpportunityNoteOut)
def create_note(opportunity_id: int, payload: OpportunityNoteCreate, db: Session = Depends(get_db)):
    if not db.get(Opportunity, opportunity_id):
        raise HTTPException(status_code=404, detail="Opportunity not found")
    note = OpportunityNote(opportunity_id=opportunity_id, note=payload.note, operator=payload.operator)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note
