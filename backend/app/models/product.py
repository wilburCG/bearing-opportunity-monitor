from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(256), index=True)
    model: Mapped[str | None] = mapped_column(String(128), index=True)
    category: Mapped[str | None] = mapped_column(String(64), index=True)
    industry: Mapped[str | None] = mapped_column(String(64), index=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"), index=True)
    manufacturer_name: Mapped[str | None] = mapped_column(String(256), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    specifications: Mapped[dict | None] = mapped_column(JSON)
    application_scenarios: Mapped[dict | None] = mapped_column(JSON)
    tags: Mapped[dict | None] = mapped_column(JSON)
    source_url: Mapped[str | None] = mapped_column(String(512))
    confidence_score: Mapped[float] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
