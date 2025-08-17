import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
import sys
import os

# добавляем backend в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.settings import get_settings
from src.database import Base, engine
from main import app


@pytest_asyncio.fixture(scope="session", autouse=True)
async def set_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session")
def client():
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        test_client.close()

@pytest.fixture(scope="session")
def config():
    return get_settings()
