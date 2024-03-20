from app.exceptions.http_exceptions import (
    DeletedError,
    InvalidIDTypeError,
    InvalidPathError,
    NoteNotFoundError,
)


class TestGetMethod:
    async def test_get_note(self, test_client, note):
        response = await test_client.get_note(note['id'])

        assert response.status_code == 200
        json = response.json()
        assert json

        assert json.get('title') == note.get('title')
        assert json.get('body') == note.get('body')
        assert json.get('created_at') == note.get('created_at')
        assert json.get('updated_at') == note.get('updated_at')
        assert json.get('deleted_at') == note.get('deleted_at')

    async def test_get_note_with_wrong_id(self, test_client):
        response = await test_client.get_note(-1)

        assert response.status_code == NoteNotFoundError.code
        json = response.json()
        assert json
        assert json.get('error_code') == NoteNotFoundError.json.error_code

    async def test_get_note_with_wrong_id_type(self, test_client):
        response = await test_client.get_note('string')

        assert response.status_code == InvalidIDTypeError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidIDTypeError.json.error_code

    async def test_get_deleted_note(self, test_client, note):
        note_id = note.get('id')
        await test_client.delete_note(note_id)
        response = await test_client.get_note(note_id)

        assert response.status_code == DeletedError.code
        json = response.json()
        assert json
        assert json.get('error_code') == DeletedError.json.error_code

    async def test_get_method_with_unexciting_path(self, test_client):
        response = await test_client.test_client.get('/nonexistent/path')

        assert response.status_code == InvalidPathError.code
        json = response.json()
        assert json
        assert json.get('error_code') == InvalidPathError.json.error_code
