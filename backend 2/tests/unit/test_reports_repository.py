from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.repositories.reports import ReportRepository


class FakeExecuteResult:
    def __init__(self, *, one=None):
        self._one = one

    def one(self):
        return self._one


@pytest.mark.asyncio
async def test_get_aggregated_stats() -> None:
    session = AsyncMock()
    session.execute = AsyncMock(
        return_value=FakeExecuteResult(
            one=SimpleNamespace(
                municipality_count=43,
                avg_birth_rate=10.3,
                avg_death_rate=12.2,
                avg_migration=461,
                avg_population=120000,
                sum_population=5_100_000,
            ),
        ),
    )

    repo = ReportRepository(session)
    stats = await repo.get_aggregated_stats(
        region='Московская область',
        municipality_type='city',
        year_from=2019,
        year_to=2023,
    )

    assert stats['municipality_count'] == 43
    assert stats['avg_birth_rate'] == 10.3
    assert stats['avg_death_rate'] == 12.2
