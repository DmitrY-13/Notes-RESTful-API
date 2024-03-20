from pydantic import BaseModel, SerializeAsAny

from .error_descriptions_schemas import ErrorDescriptionSchema


class ErrorSchema(BaseModel):
    error_code: str
    description: SerializeAsAny[ErrorDescriptionSchema] | None = None
