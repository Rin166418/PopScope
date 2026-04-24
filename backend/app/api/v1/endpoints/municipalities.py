from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_municipality_data_repository, get_municipality_repository
from app.repositories.municipalities import MunicipalityDataRepository, MunicipalityRepository
from app.schemas.municipality import MunicipalityListResponse, MunicipalityRead
from app.schemas.municipality_data import MunicipalityDataListResponse, MunicipalityDataRead

router = APIRouter(prefix='/municipalities', tags=['municipalities'])


@router.get('', response_model=MunicipalityListResponse)
async def list_municipalities(
    region: str | None = None,
    type: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    repository: MunicipalityRepository = Depends(get_municipality_repository),
) -> MunicipalityListResponse:
    items, total = await repository.list_municipalities(
        region=region,
        municipality_type=type,
        limit=limit,
        offset=offset,
    )
    return MunicipalityListResponse(
        items=[MunicipalityRead.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get('/{municipality_id}', response_model=MunicipalityRead)
async def get_municipality(
    municipality_id: int,
    repository: MunicipalityRepository = Depends(get_municipality_repository),
) -> MunicipalityRead:
    municipality = await repository.get_municipality(municipality_id)
    if municipality is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Municipality not found',
        )
    return MunicipalityRead.model_validate(municipality)


@router.get('/{municipality_id}/data', response_model=MunicipalityDataListResponse)
async def get_municipality_data(
    municipality_id: int,
    year_from: int | None = Query(default=None),
    year_to: int | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=5000),
    offset: int = Query(default=0, ge=0),
    repository: MunicipalityDataRepository = Depends(get_municipality_data_repository),
) -> MunicipalityDataListResponse:
    items, total = await repository.list_data(
        municipality_id=municipality_id,
        region=None,
        municipality_type=None,
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
