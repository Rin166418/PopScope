from fastapi import APIRouter, Depends, Query

from app.api.deps import get_municipality_data_repository
from app.repositories.municipalities import MunicipalityDataRepository
from app.schemas.municipality_data import MunicipalityDataListResponse, MunicipalityDataRead

router = APIRouter(prefix='/municipality-data', tags=['municipality-data'])


@router.get('', response_model=MunicipalityDataListResponse)
async def list_municipality_data(
    region: str | None = None,
    type: str | None = Query(default=None),
    year_from: int | None = Query(default=None),
    year_to: int | None = Query(default=None),
    limit: int = Query(default=500, ge=1, le=5000),
    offset: int = Query(default=0, ge=0),
    repository: MunicipalityDataRepository = Depends(get_municipality_data_repository),
) -> MunicipalityDataListResponse:
    items, total = await repository.list_data(
        municipality_id=None,
        region=region,
        municipality_type=type,
        year_from=year_from,
        year_to=year_to,
        limit=limit,
        offset=offset,
    )
    return MunicipalityDataListResponse(
        items=[MunicipalityDataRead.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )
