from starlette import status

from app.configs.note_config import NoteConfig
from app.routing.schemas.error_schemas.error_descriptions_schemas import (
    LengthErrorDescriptionSchema,
    TypeErrorDescriptionSchema,
)
from app.routing.schemas.error_schemas.error_schemas import ErrorSchema


class HTTPError(Exception):
    code: status
    json: ErrorSchema


class BadRequestError(HTTPError):
    code = status.HTTP_400_BAD_REQUEST


class NotFoundError(HTTPError):
    code = status.HTTP_404_NOT_FOUND


class UnprocessableEntity(HTTPError):
    code = status.HTTP_422_UNPROCESSABLE_ENTITY


class DeletedError(HTTPError):
    code = status.HTTP_410_GONE

    json = ErrorSchema(error_code='note_deleted')


class InternalServerError(HTTPError):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    json = ErrorSchema(error_code='internal_server_error')


class InvalidIDTypeError(UnprocessableEntity):
    json = ErrorSchema(error_code='invalid_id_type')


class InvalidTitleTypeError(UnprocessableEntity):
    json = ErrorSchema(
        error_code='invalid_title_type',
        description=TypeErrorDescriptionSchema(expectable_type='string'),
    )


class InvalidBodyTypeError(UnprocessableEntity):
    json = ErrorSchema(
        error_code='invalid_body_type',
        description=TypeErrorDescriptionSchema(expectable_type='string'),
    )


class InvalidTitleLengthError(UnprocessableEntity):
    json = ErrorSchema(
        error_code='invalid_title_length',
        description=LengthErrorDescriptionSchema(
            min_length=NoteConfig.title_min_length,
            max_length=NoteConfig.title_max_length,
        ),
    )


class InvalidBodyLengthError(UnprocessableEntity):
    json = ErrorSchema(
        error_code='invalid_body_length',
        description=LengthErrorDescriptionSchema(
            min_length=None, max_length=NoteConfig.body_max_length
        ),
    )


class MissingTitleError(BadRequestError):
    json = ErrorSchema(error_code='missing_title')


class MissingJSONError(BadRequestError):
    json = ErrorSchema(error_code='missing_json')


class InvalidJSONError(BadRequestError):
    json = ErrorSchema(error_code='invalid_json')


class InvalidRequestBodyError(BadRequestError):
    json = ErrorSchema(error_code='invalid_request_body')


class NoteNotFoundError(NotFoundError):
    json = ErrorSchema(error_code='note_not_found')


class InvalidPathError(NotFoundError):
    json = ErrorSchema(error_code='invalid_path')


class MethodNotAllowedError(HTTPError):
    code = status.HTTP_405_METHOD_NOT_ALLOWED
    json = ErrorSchema(error_code='method_not_allowed')
