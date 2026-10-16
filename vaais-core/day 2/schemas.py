
from fastapi import FastAPI
from typing import Literal
from pydantic import BaseModel, Field, field_validator


app = FastAPI(
    title="Lead Extraction API",
    description="API for extracting lead information",
    version="1.0.0"
)


class ExtractRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=2000,
        description="Text to extract lead information from"
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Text cannot contain only whitespace")
        return value


class LeadFields(BaseModel):
    travelers: int | None = Field(
        default=None,
        gt=0,
        description="Number of travelers must be greater than zero"
    )

    dates: str | None = None
    location: str | None = None
    duration: str | None = None
    origin_country: str | None = None

    price: float | None = Field(
        default=None,
        ge=0,
        description="Price must be zero or greater"
    )

    needs_review: bool | None = None


class ExtractionResponse(BaseModel):
    status: Literal["success", "partial", "error"]
    data: LeadFields | None = None
    error: str | None = None
    warnings: list[str] = Field(default_factory=list)


@app.get("/")
async def home():
    return {"message": "Lead Extraction API is running"}


@app.post("/extract", response_model=ExtractionResponse)
def extract_lead(request: ExtractRequest):
    # Right now it just returns an empty LeadFields() object!
    return ExtractionResponse(
        status="success",
        data=LeadFields()
    )


