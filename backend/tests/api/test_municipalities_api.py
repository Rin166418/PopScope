from dataclasses import dataclass

import pytest

from app.api.deps import get_municipality_data_repository, get_municipality_repository


@dataclass
class FakeMunicipality:
    id: int
    name: str
    region: str
    type: str
    area: float | None = None


@dataclass
class FakeMunicipalityData:
    id: int
    municipality_id: int
    year: int
    population: int
    birth_rate: float
    death_rate: float
    migration: int


class FakeMunicipalityRepo:
    async def list_municipalities(self, **kwargs):
        return [FakeMunicipality(1, 'Казань', 'Республика Татарстан', 'city', 425.3)], 1

    async def get_municipality(self, municipality_id: int):
        if municipality_id == 1:
            return FakeMunicipality(1, 'Казань', 'Республика Татарстан', 'city', 425.3)
        return None


class FakeMunicipalityDataRepo:
    async def list_data(self, **kwargs):
        return [
            FakeMunicipalityData(
                id=1,
                municipality_id=1,
                year=2023,
                population=1300000,
                birth_rate=10.5,
                death_rate=12.3,
                migration=500,
            ),
        ], 1


@pytest.mark.asyncio
async def test_list_municipalities(client, app) -> None:
    app.dependency_overrides[get_municipality_repository] = lambda: FakeMunicipalityRepo()

    response = await client.get('/api/v1/municipalities?limit=10&offset=0')
    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload['total'] == 1
    assert payload['items'][0]['name'] == 'Казань'


@pytest.mark.asyncio
async def test_get_municipality_not_found(client, app) -> None:
    app.dependency_overrides[get_municipality_repository] = lambda: FakeMunicipalityRepo()

    response = await client.get('/api/v1/municipalities/999')
    app.dependency_overrides.clear()

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_municipality_data(client, app) -> None:
    app.dependency_overrides[get_municipality_data_repository] = lambda: FakeMunicipalityDataRepo()

    response = await client.get('/api/v1/municipalities/1/data?year_from=2020&year_to=2023')
    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload['items'][0]['year'] == 2023
    assert payload['items'][0]['population'] == 1300000
