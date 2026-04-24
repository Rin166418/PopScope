from sqlalchemy import Select, and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Municipality, MunicipalityData


class MunicipalityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_municipalities(
        self,
        *,
        region: str | None,
        municipality_type: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[Municipality], int]:
        filters = []
        if region:
            filters.append(Municipality.region == region)
        if municipality_type:
            filters.append(Municipality.type == municipality_type)

        stmt: Select[tuple[Municipality]] = select(Municipality)
        if filters:
            stmt = stmt.where(and_(*filters))
        stmt = stmt.order_by(Municipality.name.asc()).limit(limit).offset(offset)

        count_stmt = select(func.count(Municipality.id))
        if filters:
            count_stmt = count_stmt.where(and_(*filters))

        result = await self.session.execute(stmt)
        total_result = await self.session.execute(count_stmt)
        return list(result.scalars().all()), int(total_result.scalar_one())

    async def get_municipality(self, municipality_id: int) -> Municipality | None:
        result = await self.session.execute(
            select(Municipality).where(Municipality.id == municipality_id),
        )
        return result.scalar_one_or_none()


class MunicipalityDataRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_data(
        self,
        *,
        municipality_id: int | None,
        region: str | None,
        municipality_type: str | None,
        year_from: int | None,
        year_to: int | None,
        limit: int,
        offset: int,
    ) -> tuple[list[MunicipalityData], int]:
        stmt = select(MunicipalityData).join(Municipality)
        count_stmt = select(func.count(MunicipalityData.id)).join(Municipality)

        filters = []
        if municipality_id is not None:
            filters.append(MunicipalityData.municipality_id == municipality_id)
        if region:
            filters.append(Municipality.region == region)
        if municipality_type:
            filters.append(Municipality.type == municipality_type)
        if year_from is not None:
            filters.append(MunicipalityData.year >= year_from)
        if year_to is not None:
            filters.append(MunicipalityData.year <= year_to)

        if filters:
            stmt = stmt.where(and_(*filters))
            count_stmt = count_stmt.where(and_(*filters))

        stmt = (
            stmt.order_by(MunicipalityData.year.asc(), MunicipalityData.municipality_id.asc())
            .limit(limit)
            .offset(offset)
        )

        rows = await self.session.execute(stmt)
        total = await self.session.execute(count_stmt)
        return list(rows.scalars().all()), int(total.scalar_one())
