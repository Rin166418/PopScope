from fastapi import APIRouter, Depends

from app.api.deps import get_report_service
from app.schemas.report import AnalyticsReportRequest, AnalyticsReportResponse
from app.services.reports import AnalyticsReportService

router = APIRouter(prefix='/reports', tags=['reports'])


@router.post('/analytics', response_model=AnalyticsReportResponse)
async def generate_analytics_report(
    payload: AnalyticsReportRequest,
    service: AnalyticsReportService = Depends(get_report_service),
) -> AnalyticsReportResponse:
    return await service.generate_report(payload)
