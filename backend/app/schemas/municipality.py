from pydantic import BaseModel, Field


class MunicipalityBase(BaseModel):
    name: str
    region: str
    type: str
    area: float | None = None


class MunicipalityRead(MunicipalityBase):
    id: int

    model_config = {'from_attributes': True}


class MunicipalityListResponse(BaseModel):
    items: list[MunicipalityRead]
    total: int = Field(ge=0)
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)
