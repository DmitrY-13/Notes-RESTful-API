from json import JSONDecodeError

from app.exceptions.http_exceptions import (
    InvalidIDTypeError,
    InvalidPathError,
    NoteNotFoundError,
)


class TestDeleteMethod:
    async def test_delete_note(self, test_client, note):
        response = await test_client.delete_note(note['id'])

        assert response.status_code == 204

        json = None
        try:
            json = response.json()
        except JSONDecodeError:
            pass
        assert json is None

    async def test_delete_note_with_wrong_id(self, test_client):
        response = await test_client.delete_note(-1)

        assert response.status_code == NoteNotFoundError.code
        json = response.json()
        assert json
        assert json.get('error_code') == NoteNotFoundError.json.error_code

    async def test_delete_note_with_wrong_id_type(self, test_client):
        response = await test_client.delete_note('wrong_id')

        assert response.status_code == InvalidIDTypeError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidIDTypeError.json.error_code

    async def test_delete_method_with_unexciting_path(self, test_client):
        response = await test_client.test_client.delete('/nonexistent/path')

        assert response.status_code == InvalidPathError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidPathError.json.error_code
