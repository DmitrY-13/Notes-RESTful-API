from pydantic import BaseModel


class ErrorDescriptionSchema(BaseModel):
    pass


class LengthErrorDescriptionSchema(ErrorDescriptionSchema):
    min_length: int | None = None
    max_length: int


class TypeErrorDescriptionSchema(ErrorDescriptionSchema):
    expectable_type: str
