from re import match

import pendulum
import pytest

from app.configs.note_config import NoteConfig
from app.exceptions.http_exceptions import (
    InvalidBodyLengthError,
    InvalidBodyTypeError,
    InvalidPathError,
    InvalidTitleLengthError,
    InvalidTitleTypeError,
    MissingTitleError,
)
from tests.test_data import ISO_8601_REGEX, InvalidJSON, ValidJSON


class TestPostMethod:
    @pytest.mark.parametrize(
        'request_json',
        (ValidJSON.min_title(), ValidJSON.max_values()),
        ids=('min title', 'max values'),
    )
    async def test_post_note(self, test_client, request_json):
        response = await test_client.post_note(request_json)

        assert response.status_code == 201
        json = response.json()
        assert json

        assert json.get('title') == request_json.get('title')

        if request_json.get('body') is None:
            assert json.get('body') == ''
        else:
            assert json.get('body') == request_json.get('body')

        created_at = json.get('created_at')
        assert match(ISO_8601_REGEX, created_at)
        assert pendulum.parse(created_at).diff(pendulum.now()).in_seconds() < 2

        assert json.get('updated_at') is None
        assert json.get('deleted_at') is None

    async def test_post_note_with_invalid_title_type(self, test_client):
        response = await test_client.post_note(
            InvalidJSON.invalid_title_type()
        )

        assert response.status_code == InvalidTitleTypeError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidTitleTypeError.json.error_code

    async def test_post_note_with_invalid_body_type(self, test_client):
        response = await test_client.post_note(InvalidJSON.invalid_body_type())

        assert response.status_code == InvalidBodyTypeError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidBodyTypeError.json.error_code

    async def test_post_note_with_missing_note_title(self, test_client):
        response = await test_client.post_note({})

        assert response.status_code == MissingTitleError.code
        json = response.json()
        assert json
        assert json.get('error_code') == MissingTitleError.json.error_code

    @pytest.mark.parametrize(
        'request_json',
        (InvalidJSON.too_short_title(), InvalidJSON.too_long_title()),
        ids=('too short title', 'too long title'),
    )
    async def test_post_note_with_invalid_title_length(
        self, test_client, request_json
    ):
        response = await test_client.post_note(request_json)

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

    async def test_post_note_with_mote_than_max_length_note_body(
        self, test_client
    ):
        response = await test_client.post_note(InvalidJSON.too_long_body())

        assert response.status_code == InvalidBodyLengthError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidBodyLengthError.json.error_code
        description = json.get('description')
        assert description
        assert description.get('max_length') == NoteConfig.body_max_length

    async def test_post_method_with_unexciting_path(self, test_client):
        response = await test_client.test_client.post('/nonexistent/path')

        assert response.status_code == InvalidPathError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidPathError.json.error_code
