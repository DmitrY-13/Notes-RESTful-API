from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict

from app.configs.note_config import NoteConfig
from app.exceptions.http_exceptions import (
    InvalidBodyLengthError,
    InvalidBodyTypeError,
    InvalidTitleLengthError,
    InvalidTitleTypeError,
)


class NoteRequestSchema(BaseModel):
    title: str
    body: Optional[str] = ''

    @field_validator('title', mode='before')
    @classmethod
    def check_title(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise InvalidTitleTypeError()

        value_length = len(value)

        if (
            value_length < NoteConfig.title_min_length
            or value_length > NoteConfig.title_max_length
        ):
            raise InvalidTitleLengthError()

        return value

    @field_validator('body', mode='before')
    @classmethod
    def check_body(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise InvalidBodyTypeError()

        if len(value) > NoteConfig.body_max_length:
            raise InvalidBodyLengthError()

        return value


class NoteResponseSchema(BaseModel):
    id: int
    title: str = Field(
        min_length=NoteConfig.title_min_length,
        max_length=NoteConfig.title_max_length,
    )
    body: str = Field(max_length=NoteConfig.body_max_length)

    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
