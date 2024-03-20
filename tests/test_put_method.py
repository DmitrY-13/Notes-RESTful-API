from re import match

import pendulum
import pytest
from test_data import ISO_8601_REGEX, InvalidJSON, ValidJSON

from app.configs.note_config import NoteConfig
from app.exceptions.http_exceptions import (
    InvalidBodyLengthError,
    InvalidBodyTypeError,
    InvalidIDTypeError,
    InvalidPathError,
    InvalidTitleLengthError,
    InvalidTitleTypeError,
    NoteNotFoundError,
)


class TestPutMethod:
    @pytest.mark.parametrize(
        'request_json',
        (ValidJSON.min_title(), ValidJSON.max_values()),
        ids=('min title', 'max values'),
    )
    async def test_put_note(self, test_client, note, request_json):
        response = await test_client.put_note(note['id'], request_json)

        assert response.status_code == 200
        json = response.json()
        assert json

        assert json.get('id') == note.get('id')
        assert json.get('title') == request_json['title']
        if request_json.get('body'):
            assert json.get('body') == request_json['body']
        assert json.get('created_at') == note.get('created_at')
        updated_at = json.get('updated_at')
        assert updated_at
        assert match(ISO_8601_REGEX, updated_at)
        assert pendulum.parse(updated_at).diff(pendulum.now()).in_seconds() < 2
        assert json.get('deleted_at') == note.get('deleted_at')

    async def test_put_note_with_invalid_title_type(self, test_client, note):
        response = await test_client.put_note(
            note['id'], InvalidJSON.invalid_title_type()
        )

        assert response.status_code == InvalidTitleTypeError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidTitleTypeError.json.error_code

    async def test_put_note_with_invalid_body_type(self, test_client, note):
        response = await test_client.put_note(
            note['id'], InvalidJSON.invalid_body_type()
        )

        assert response.status_code == InvalidBodyTypeError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidBodyTypeError.json.error_code

    @pytest.mark.parametrize(
        'request_json',
        (InvalidJSON.too_short_title(), InvalidJSON.too_long_title()),
        ids=('too short title', 'too long title'),
    )
    async def test_put_note_with_invalid_title_length(
        self, test_client, note, request_json
    ):
        response = await test_client.put_note(
            note['id'], InvalidJSON.too_short_title()
        )

        assert response.status_code == InvalidTitleLengthError.code
        json = response.json()
        assert json
        assert (
            json.get('error_code') == InvalidTitleLengthError.json.error_code
        )
        description = json.get('description')
        assert description
        assert description.get('min_length') == NoteConfig.title_min_length
        assert description.get('max_length') == NoteConfig.title_max_length

    async def test_put_note_with_invalid_body_length(self, note, test_client):
        response = await test_client.put_note(
            note['id'], InvalidJSON.too_long_body()
        )

        assert response.status_code == InvalidBodyLengthError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidBodyLengthError.json.error_code
        description = json.get('description')
        assert description
        assert description.get('max_length') == NoteConfig.body_max_length

    async def test_put_note_with_wrong_id(self, test_client):
        response = await test_client.put_note(-1, ValidJSON.min_title())

        assert response.status_code == NoteNotFoundError.code
        json = response.json()
        assert json
        assert json.get('error_code') == NoteNotFoundError.json.error_code

    async def test_put_note_with_wrong_id_type(self, test_client):
        response = await test_client.put_note('string', ValidJSON.min_title())

        assert response.status_code == InvalidIDTypeError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidIDTypeError.json.error_code

    async def test_put_method_with_unexciting_path(self, test_client):
        response = await test_client.test_client.put('/nonexistent/path')

        assert response.status_code == InvalidPathError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidPathError.json.error_code
