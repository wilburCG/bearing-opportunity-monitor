from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(512), index=True)
    summary: Mapped[str | None] = mapped_column(Text)
    opportunity_type: Mapped[str | None] = mapped_column(String(64), index=True)
    industry: Mapped[str | None] = mapped_column(String(64), index=True)
    company_name: Mapped[str | None] = mapped_column(String(256), index=True)
    project_name: Mapped[str | None] = mapped_column(String(256))
    province: Mapped[str | None] = mapped_column(String(64), index=True)
    city: Mapped[str | None] = mapped_column(String(64), index=True)
    district: Mapped[str | None] = mapped_column(String(64))
    address: Mapped[str | None] = mapped_column(String(512))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    bearing_types: Mapped[dict | None] = mapped_column(JSON)
    bearing_models: Mapped[dict | None] = mapped_column(JSON)
    equipment_types: Mapped[dict | None] = mapped_column(JSON)
    estimated_quantity: Mapped[str | None] = mapped_column(String(128))
    estimated_amount: Mapped[str | None] = mapped_column(String(128))
    deadline_at: Mapped[datetime | None] = mapped_column(DateTime)
    volume_score: Mapped[float] = mapped_column(Float, default=0)
    urgency_score: Mapped[float] = mapped_column(Float, default=0)
    confidence_score: Mapped[float] = mapped_column(Float, default=0)
    fit_score: Mapped[float] = mapped_column(Float, default=0)
    total_score: Mapped[float] = mapped_column(Float, default=0, index=True)
    confidence_reason: Mapped[str | None] = mapped_column(Text)
    recommended_action: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="new", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
