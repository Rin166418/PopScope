from typing import Any

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Municipality, MunicipalityData


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_aggregated_stats(
        self,
        *,
        region: str | None,
        municipality_type: str | None,
        year_from: int,
        year_to: int,
    ) -> dict[str, Any]:
        filters = [
            MunicipalityData.year >= year_from,
            MunicipalityData.year <= year_to,
        ]
        if region:
            filters.append(Municipality.region == region)
        if municipality_type:
            filters.append(Municipality.type == municipality_type)

        stmt = (
            select(
                func.count(func.distinct(Municipality.id)).label('municipality_count'),
                func.avg(MunicipalityData.birth_rate).label('avg_birth_rate'),
                func.avg(MunicipalityData.death_rate).label('avg_death_rate'),
                func.avg(MunicipalityData.migration).label('avg_migration'),
                func.avg(MunicipalityData.population).label('avg_population'),
                func.sum(MunicipalityData.population).label('sum_population'),
            )
            .select_from(MunicipalityData)
            .join(Municipality, Municipality.id == MunicipalityData.municipality_id)
            .where(and_(*filters))
        )

        result = await self.session.execute(stmt)
        row = result.one()

        return {
            'municipality_count': int(row.municipality_count or 0),
            'avg_birth_rate': float(row.avg_birth_rate or 0),
            'avg_death_rate': float(row.avg_death_rate or 0),
            'avg_migration': float(row.avg_migration or 0),
            'avg_population': float(row.avg_population or 0),
            'sum_population': float(row.sum_population or 0),
        }
