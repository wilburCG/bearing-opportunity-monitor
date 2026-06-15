from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    alias_names: Mapped[dict | None] = mapped_column(JSON)
    company_type: Mapped[str | None] = mapped_column(String(64), index=True)
    industry: Mapped[str | None] = mapped_column(String(64), index=True)
    province: Mapped[str | None] = mapped_column(String(64), index=True)
    city: Mapped[str | None] = mapped_column(String(64), index=True)
    address: Mapped[str | None] = mapped_column(String(512))
    website: Mapped[str | None] = mapped_column(String(512))
    description: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[dict | None] = mapped_column(JSON)
    source_url: Mapped[str | None] = mapped_column(String(512))
    confidence_score: Mapped[float] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
