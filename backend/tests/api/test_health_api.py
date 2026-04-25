from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock

import pytest

from app.db.session import get_db


@pytest.mark.asyncio
async def test_live_endpoint(client) -> None:
    response = await client.get('/api/v1/health/live')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


@pytest.mark.asyncio
async def test_ready_endpoint(client, app) -> None:
    fake_session = AsyncMock()
    fake_session.execute = AsyncMock()

    async def override_db() -> AsyncGenerator[AsyncMock, None]:
        yield fake_session

    app.dependency_overrides[get_db] = override_db
    response = await client.get('/api/v1/health/ready')
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {'status': 'ready'}
    fake_session.execute.assert_awaited_once()
