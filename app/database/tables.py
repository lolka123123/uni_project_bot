from sqlalchemy import DateTime, Table, ForeignKey, Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from app.database.settings import Base

class Admin(Base):
    __tablename__ = "admin"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True)




audio_tags = Table(
    "audio_tags",
    Base.metadata,
    Column("audio_id", ForeignKey("audios.id", ondelete='CASCADE'), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete='CASCADE'), primary_key=True),
)

class Audio(Base):
    __tablename__ = "audios"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int]
    username: Mapped[str]
    audio_name: Mapped[str]
    audio_url: Mapped[str]
    tags: Mapped[list['Tag']] = relationship('Tag', secondary=audio_tags, back_populates='audios')
    views: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    audios: Mapped[list[Audio]] = relationship("Audio", secondary=audio_tags, back_populates="tags")