from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class SearchTask(Base):
    __tablename__ = "search_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_type: Mapped[str] = mapped_column(String(64), index=True)
    query: Mapped[str] = mapped_column(String(512), index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
    found_count: Mapped[int] = mapped_column(Integer, default=0)
    created_opportunity_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
