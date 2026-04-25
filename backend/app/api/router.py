from fastapi import APIRouter

from app.api.v1.endpoints import health, municipalities, municipality_data, predictions, reports

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(municipalities.router)
api_router.include_router(municipality_data.router)
api_router.include_router(predictions.router)
api_router.include_router(reports.router)
