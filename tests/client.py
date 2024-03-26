from httpx import AsyncClient, ASGITransport

from app.routing.routing import app


class Client:
    _path = '/api/v1/notes'
    _path_with_id = 'api/v1/notes/{}'

    def __init__(self):
        self.test_client = AsyncClient(transport=ASGITransport(app=app), base_url='http://test')

    async def __aenter__(self):
        await self.test_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.test_client.__aexit__(exc_type, exc_val, exc_tb)

    async def get_note(self, note_id):
        path = self._path_with_id.format(note_id)
        return await self.test_client.get(url=path)

    async def post_note(self, json):
        return await self.test_client.post(url=self._path, json=json)

    async def put_note(self, note_id, json):
        path = self._path_with_id.format(note_id)
        return await self.test_client.put(url=path, json=json)

    async def delete_note(self, note_id):
        path = self._path_with_id.format(note_id)
        return await self.test_client.delete(path)
