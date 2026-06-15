from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class EntityRelationship(Base):
    __tablename__ = "entity_relationships"
    __table_args__ = (
        UniqueConstraint("source_type", "source_id", "target_type", "target_id", "relation_type", name="uq_entity_relationship"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_type: Mapped[str] = mapped_column(String(32), index=True)  # company/product/opportunity
    source_id: Mapped[int] = mapped_column(Integer, index=True)
    target_type: Mapped[str] = mapped_column(String(32), index=True)  # company/product/opportunity
    target_id: Mapped[int] = mapped_column(Integer, index=True)
    relation_type: Mapped[str] = mapped_column(String(64), index=True)  # manufactures/mentions/buys/supplies/competes/used_in
    evidence: Mapped[str | None] = mapped_column(Text)
    confidence_score: Mapped[float] = mapped_column(Float, default=0)
    source_url: Mapped[str | None] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
