from pydantic import BaseModel, Field, model_validator


class AnalyticsReportRequest(BaseModel):
    region: str | None = None
    municipality_type: str | None = Field(default=None, alias='type')
    year_from: int = Field(default=2019, ge=1900)
    year_to: int = Field(default=2023, ge=1900)

    @model_validator(mode='after')
    def validate_year_range(self) -> 'AnalyticsReportRequest':
        if self.year_to < self.year_from:
            raise ValueError('year_to must be greater than or equal to year_from')
        return self


class AnalyticsReportResponse(BaseModel):
    provider: str
    model_name: str | None = None
    region: str | None = None
    municipality_type: str | None = None
    year_from: int
    year_to: int
    report_text: str
