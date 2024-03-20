from fastapi import Request
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.responses import JSONResponse

from app.exceptions.http_exceptions import (
    HTTPError,
    InternalServerError,
    InvalidIDTypeError,
    InvalidJSONError,
    InvalidPathError,
    InvalidRequestBodyError,
    MethodNotAllowedError,
    MissingJSONError,
    MissingTitleError,
)


async def http_error_handler(_, exc: HTTPError) -> JSONResponse:
    return JSONResponse(status_code=exc.code, content=exc.json.model_dump())


async def fastapi_starlette_http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    code = exc.status_code

    if code == 404:
        return await http_error_handler(request, InvalidPathError())

    if code == 405:
        return await http_error_handler(request, MethodNotAllowedError())

    return await http_error_handler(request, InternalServerError())


async def fastapi_request_validator_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()[0]

    if errors['type'] == 'int_parsing' and errors['loc'] == (
        'path',
        'note_id',
    ):
        return await http_error_handler(request, InvalidIDTypeError())

    if errors['type'] == 'model_attributes_type':
        return await http_error_handler(request, InvalidRequestBodyError())

    if errors['type'] == 'json_invalid':
        return await http_error_handler(request, InvalidJSONError())

    if errors['type'] == 'missing':
        if errors['input'] is None:
            return await http_error_handler(request, MissingJSONError())

        return await http_error_handler(request, MissingTitleError())

    return await http_error_handler(request, InternalServerError())


async def any_exception_handler(request: Request, _) -> JSONResponse:
    return await http_error_handler(request, InternalServerError())
