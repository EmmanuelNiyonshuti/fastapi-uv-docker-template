import os
from collections.abc import AsyncGenerator

os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")
os.environ.setdefault("POSTGRES_SERVER", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5434")
os.environ.setdefault("POSTGRES_DB", "test")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-not-for-production")

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.deps import get_db
from app.core.db import async_engine, metadata, user_table
from app.main import app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient]:
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        await conn.execute(user_table.delete())

    async def override_get_db() -> AsyncGenerator:
        async with async_engine.connect() as conn:
            yield conn

    app.dependency_overrides[get_db] = override_get_db
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        await async_engine.dispose()
