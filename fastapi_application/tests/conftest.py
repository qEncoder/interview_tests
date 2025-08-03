import pytest, os

from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from qhapp.main import app as etiket_app

@pytest.fixture(scope='session')
async def app():
    async with LifespanManager(etiket_app) as manager:
        yield manager.app

@pytest.fixture(scope='session')
async def async_client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client