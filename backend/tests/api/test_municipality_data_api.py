from dataclasses import dataclass

import pytest

from app.api.deps import get_municipality_data_repository


@dataclass
class FakeMunicipalityData:
    id: int
    municipality_id: int
    year: int
    population: int
    birth_rate: float
    death_rate: float
    migration: int


class FakeMunicipalityDataRepo:
    async def list_data(self, **kwargs):
        return [
            FakeMunicipalityData(
                id=2,
                municipality_id=10,
                year=2022,
                population=50000,
                birth_rate=9.9,
                death_rate=11.5,
                migration=100,
            ),
        ], 1


@pytest.mark.asyncio
async def test_list_municipality_data(client, app) -> None:
    app.dependency_overrides[get_municipality_data_repository] = lambda: FakeMunicipalityDataRepo()

    response = await client.get('/api/v1/municipality-data?region=all&year_from=2020&year_to=2023')
    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload['total'] == 1
    assert payload['items'][0]['year'] == 2022
