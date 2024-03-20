from fastapi import APIRouter, Depends, FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.db.db import get_session, new_session
from app.exceptions.http_exceptions import HTTPError
from app.middleware.middleware import Middleware
from app.routing.error_handlers import (
    any_exception_handler,
    fastapi_request_validator_error_handler,
    fastapi_starlette_http_exception_handler,
    http_error_handler,
)
from app.routing.schemas.note_schemas import (
    NoteRequestSchema,
    NoteResponseSchema,
)

app = FastAPI()
router = APIRouter(prefix='/api/v1')


@router.post('/notes', status_code=HTTP_201_CREATED)
async def post_note(
    note: NoteRequestSchema, session: new_session = Depends(get_session)
) -> NoteResponseSchema:
    note_id = await Middleware.add(note, session)
    return await Middleware.get(note_id, session)


@router.get('/notes/{note_id}', status_code=HTTP_200_OK)
async def get_note(
    note_id: int, session: new_session = Depends(get_session)
) -> NoteResponseSchema:
    return await Middleware.get(note_id, session)


@router.put('/notes/{note_id}', status_code=HTTP_200_OK)
async def put_note(
    note_id: int,
    note: NoteRequestSchema,
    session: new_session = Depends(get_session),
) -> NoteResponseSchema:
    await Middleware.update(note_id, note, session)
    return await Middleware.get(note_id, session)


@router.delete('/notes/{note_id}', status_code=HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int, session: new_session = Depends(get_session)
):
    await Middleware.delete(note_id, session)


app.add_exception_handler(HTTPError, http_error_handler)
app.add_exception_handler(
    StarletteHTTPException, fastapi_starlette_http_exception_handler
)
app.add_exception_handler(
    RequestValidationError, fastapi_request_validator_error_handler
)
app.add_exception_handler(Exception, any_exception_handler)

app.include_router(router)
