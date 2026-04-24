from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.repositories.municipalities import MunicipalityDataRepository, MunicipalityRepository
from app.repositories.predictions import PredictionRepository
from app.repositories.reports import ReportRepository
from app.services.llm import build_llm_client
from app.services.reports import AnalyticsReportService


async def get_settings_dep() -> Settings:
    return get_settings()


async def get_municipality_repository(
    session: AsyncSession = Depends(get_db),
) -> MunicipalityRepository:
    return MunicipalityRepository(session)


async def get_municipality_data_repository(
    session: AsyncSession = Depends(get_db),
) -> MunicipalityDataRepository:
    return MunicipalityDataRepository(session)


async def get_prediction_repository(
    session: AsyncSession = Depends(get_db),
) -> PredictionRepository:
    return PredictionRepository(session)


async def get_report_repository(
    session: AsyncSession = Depends(get_db),
) -> ReportRepository:
    return ReportRepository(session)


async def get_report_service(
    repository: ReportRepository = Depends(get_report_repository),
    settings: Settings = Depends(get_settings_dep),
) -> AnalyticsReportService:
    return AnalyticsReportService(repository=repository, llm_client=build_llm_client(settings))
