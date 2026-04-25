import pytest

from app.schemas.report import AnalyticsReportRequest


def test_report_request_valid_year_range() -> None:
    payload = AnalyticsReportRequest(year_from=2020, year_to=2023)
    assert payload.year_from == 2020
    assert payload.year_to == 2023


def test_report_request_invalid_year_range() -> None:
    with pytest.raises(ValueError):
        AnalyticsReportRequest(year_from=2024, year_to=2023)


def test_report_request_type_alias() -> None:
    payload = AnalyticsReportRequest.model_validate({'type': 'city'})
    assert payload.municipality_type == 'city'
