from sqlalchemy import Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class OpportunitySource(Base):
    __tablename__ = "opportunity_sources"

    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"), primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), primary_key=True)
    evidence_snippet: Mapped[str | None] = mapped_column(Text)
    extraction_confidence: Mapped[float] = mapped_column(Float, default=0)
