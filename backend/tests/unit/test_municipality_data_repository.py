from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.repositories.municipalities import MunicipalityDataRepository, MunicipalityRepository


class FakeExecuteResult:
    def __init__(self, rows):
        self._rows = rows

    def scalars(self):
        return self

    def all(self):
        return self._rows

    def scalar_one(self):
        return self._rows

    def scalar_one_or_none(self):
        return self._rows


@pytest.mark.asyncio
async def test_get_municipality() -> None:
    session = AsyncMock()
    session.execute = AsyncMock(
        return_value=FakeExecuteResult(SimpleNamespace(id=1, name='Казань')),
    )

    repo = MunicipalityRepository(session)
    municipality = await repo.get_municipality(1)

    assert municipality.id == 1


@pytest.mark.asyncio
async def test_list_data_with_filters() -> None:
    session = AsyncMock()
    session.execute = AsyncMock(
        side_effect=[
            FakeExecuteResult([SimpleNamespace(id=1, year=2022)]),
            FakeExecuteResult(1),
        ],
    )

    repo = MunicipalityDataRepository(session)
    rows, total = await repo.list_data(
        municipality_id=1,
        region='Московская область',
        municipality_type='city',
        year_from=2020,
        year_to=2023,
        limit=10,
        offset=0,
    )

    assert total == 1
    assert rows[0].year == 2022
    assert session.execute.await_count == 2
