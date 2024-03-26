from sqlalchemy import func

from app.db.db import new_session
from app.db.models import NoteModel
from app.exceptions.http_exceptions import DeletedError, NoteNotFoundError
from app.routing.schemas.note_schemas import (
    NoteRequestSchema,
    NoteResponseSchema,
)


class Middleware:
    @staticmethod
    async def add(data: NoteRequestSchema, session: new_session) -> int:
        note_dict = data.model_dump()

        note = NoteModel(**note_dict)

        session.add(note)
        await session.flush()
        await session.commit()

        return note.id

    @staticmethod
    async def _get(note_id: int, session: new_session) -> NoteModel:
        note = await session.get(NoteModel, note_id)

        if not note:
            raise NoteNotFoundError

        if note.deleted_at:
            raise DeletedError

        return note

    @classmethod
    async def get(
        cls, note_id: int, session: new_session
    ) -> NoteResponseSchema:
        note = await cls._get(note_id, session)
        return NoteResponseSchema.model_validate(note)

    @classmethod
    async def update(
        cls, note_id: int, data: NoteRequestSchema, session: new_session
    ) -> None:
        note = await cls._get(note_id, session)

        note.title = data.title
        note.body = data.body
        note.updated_at = func.now()

        await session.commit()

    @classmethod
    async def delete(cls, note_id: int, session: new_session) -> None:
        note = await cls._get(note_id, session)
        note.deleted_at = func.now()

        await session.commit()
