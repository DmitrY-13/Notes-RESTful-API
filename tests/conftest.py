import asyncio

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.db import get_session
from app.db.models import Base
from app.routing.routing import app
from tests.exceptions import NoteCreationError
from tests.test_client import TestClient
from tests.test_data import ValidJSON

engine = create_async_engine('sqlite+aiosqlite:///:memory:')
new_test_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


asyncio.run(create_tables())


async def override_get_db():
    async with new_test_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_db


@pytest.fixture(scope='session')
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_client():
    async with TestClient() as tc:
        yield tc


@pytest.fixture
async def note():
    async with TestClient() as tc:
        response = await tc.post_note(ValidJSON.max_values())

        if response.status_code != 201:
            raise NoteCreationError

        note = response.json()

        yield note

        await tc.delete_note(note['id'])
