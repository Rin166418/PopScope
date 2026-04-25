from fastapi import APIRouter, Depends, Query

from app.api.deps import get_prediction_repository
from app.repositories.predictions import PredictionRepository
from app.schemas.prediction import (
    MunicipalityPredictionCreate,
    MunicipalityPredictionListResponse,
    MunicipalityPredictionRead,
)

router = APIRouter(prefix='/predictions', tags=['predictions'])


@router.post('', response_model=MunicipalityPredictionRead)
async def create_prediction(
    payload: MunicipalityPredictionCreate,
    repository: PredictionRepository = Depends(get_prediction_repository),
) -> MunicipalityPredictionRead:
    prediction = await repository.create_prediction(payload)
    return MunicipalityPredictionRead.model_validate(prediction)


@router.get('', response_model=MunicipalityPredictionListResponse)
async def list_predictions(
    municipality_id: int | None = Query(default=None),
    model_run_id: str | None = Query(default=None),
    year_from: int | None = Query(default=None),
    year_to: int | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=2000),
    offset: int = Query(default=0, ge=0),
    repository: PredictionRepository = Depends(get_prediction_repository),
) -> MunicipalityPredictionListResponse:
    items, total = await repository.list_predictions(
        municipality_id=municipality_id,
        model_run_id=model_run_id,
        year_from=year_from,
        year_to=year_to,
        limit=limit,
        offset=offset,
    )
    return MunicipalityPredictionListResponse(
        items=[MunicipalityPredictionRead.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )
