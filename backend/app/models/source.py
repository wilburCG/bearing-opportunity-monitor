from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(512), unique=True, index=True)
    title: Mapped[str | None] = mapped_column(String(512))
    source_site: Mapped[str | None] = mapped_column(String(128), index=True)
    source_type: Mapped[str | None] = mapped_column(String(64), index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    raw_text_hash: Mapped[str | None] = mapped_column(String(64), index=True)
    content_text: Mapped[str | None] = mapped_column(Text)
    content_summary: Mapped[str | None] = mapped_column(Text)
    credibility_level: Mapped[str | None] = mapped_column(String(32))
