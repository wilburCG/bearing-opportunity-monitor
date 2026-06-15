from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class OpportunityNote(Base):
    __tablename__ = "opportunity_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"), index=True)
    note: Mapped[str] = mapped_column(Text)
    operator: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
