from datetime import datetime

from sqlalchemy import TIMESTAMP, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.configs.note_config import NoteConfig


class Base(DeclarativeBase):
    pass


class NoteModel(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(
        String(NoteConfig.title_max_length), nullable=False
    )
    body: Mapped[str] = mapped_column(
        String(NoteConfig.body_max_length), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True, server_default=None
    )
    deleted_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True, server_default=None
    )
