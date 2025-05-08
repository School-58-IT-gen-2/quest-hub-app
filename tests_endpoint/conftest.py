import pytest
from httpx import AsyncClient
from quest_hub_fastapi_server.app.fastapi import app  # Импортируйте ваш экземпляр FastAPI-приложения

@pytest.fixture(scope="session")
async def test_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client