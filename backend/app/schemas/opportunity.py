from datetime import datetime
from pydantic import BaseModel


class OpportunityOut(BaseModel):
    id: int
    title: str
    summary: str | None = None
    opportunity_type: str | None = None
    industry: str | None = None
    company_name: str | None = None
    province: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    volume_score: float
    urgency_score: float
    confidence_score: float
    fit_score: float
    total_score: float
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OpportunityDetailOut(OpportunityOut):
    project_name: str | None = None
    district: str | None = None
    address: str | None = None
    bearing_types: dict | None = None
    bearing_models: dict | None = None
    equipment_types: dict | None = None
    estimated_quantity: str | None = None
    estimated_amount: str | None = None
    deadline_at: datetime | None = None
    confidence_reason: str | None = None
    recommended_action: str | None = None


class OpportunityStatusUpdate(BaseModel):
    status: str
