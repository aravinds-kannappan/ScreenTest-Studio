from typing import Any

from pydantic import BaseModel, Field, HttpUrl, field_validator


class ScreenTestRequest(BaseModel):
    brand_pitch: str = Field(
        min_length=20,
        max_length=4000,
        description="One paragraph describing the brand, product, and target customer.",
    )
    brand_url: HttpUrl | None = Field(
        default=None,
        description="Optional website URL used by the Builder Agent for brand profiling.",
    )

    @field_validator("brand_pitch")
    @classmethod
    def normalize_pitch(cls, value: str) -> str:
        return " ".join(value.strip().split())


class ScreenTestResponse(BaseModel):
    run_id: str
    status: str
    elapsed_seconds: float
    result: dict[str, Any] | None = None
    raw_output: str
    task_outputs: list[dict[str, Any]] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    service: str
    crew_runtime: str
