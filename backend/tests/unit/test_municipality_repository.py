from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.repositories.municipalities import MunicipalityRepository


class FakeExecuteResult:
    def __init__(self, values):
        self._values = values

    def scalars(self):
        return self

    def all(self):
        return self._values

    def scalar_one(self):
        return self._values


@pytest.mark.asyncio
async def test_list_municipalities_returns_items_and_total() -> None:
    session = AsyncMock()
    session.execute = AsyncMock(
        side_effect=[
            FakeExecuteResult([SimpleNamespace(id=1, name='Казань')]),
            FakeExecuteResult(1),
        ],
    )

    repo = MunicipalityRepository(session)
    items, total = await repo.list_municipalities(
        region=None,
        municipality_type=None,
        limit=50,
        offset=0,
    )

    assert total == 1
    assert len(items) == 1
    assert items[0].name == 'Казань'
    assert session.execute.await_count == 2
