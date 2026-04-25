import pytest

from app.api.deps import get_report_service


class FakeReportService:
    async def generate_report(self, payload):
        return {
            'provider': 'stub',
            'model_name': 'stub-v1',
            'region': payload.region,
            'municipality_type': payload.municipality_type,
            'year_from': payload.year_from,
            'year_to': payload.year_to,
            'report_text': 'Тестовый отчет',
        }


@pytest.mark.asyncio
async def test_generate_report(client, app) -> None:
    app.dependency_overrides[get_report_service] = lambda: FakeReportService()

    response = await client.post(
        '/api/v1/reports/analytics',
        json={'year_from': 2019, 'year_to': 2023},
    )
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()['report_text'] == 'Тестовый отчет'


@pytest.mark.asyncio
async def test_generate_report_invalid_year_range(client) -> None:
    response = await client.post(
        '/api/v1/reports/analytics',
        json={'year_from': 2024, 'year_to': 2023},
    )

    assert response.status_code == 422
