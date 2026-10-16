
import re
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
    name: str | None = Field(
        default=None,
        description="Name of the lead"
    )
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


# Stub: extracts only information covered by simple rules
def extract_lead_stub(text: str) -> LeadFields:
    text_lower = text.lower()

    # Extract name
    name = None
    match = re.search(
        r"\b(?:i am|my name is)\s+([a-z]+(?:\s+[a-z]+)*?)(?:\s+from|\s+and|[.,!?]|$)",
        text_lower
    )
    if match:
        name = match.group(1).strip().title()

    # Extract number of travelers
    travelers = None
    match = re.search(
        r"\b(\d+)\s+(?:travelers?|people|persons?)\b",
        text_lower
    )
    if match:
        val = int(match.group(1))
        if val > 0:
            travelers = val

    # Extract destination using simple phrases
    location = None
    match = re.search(
        r"\b(?:to|visit|destination is)\s+"
        r"(skardu|hunza|lahore|islamabad|karachi)\b",
        text_lower
    )
    if match:
        location = match.group(1).title()

    # Extract price when explicitly mentioned
    price = None
    match = re.search(
        r"\b(?:budget|price|cost)\s*(?:is|of|:)?\s*"
        r"(?:rs\.?|pkr|usd|\$)?\s*(\d+(?:\.\d+)?)\b",
        text_lower
    )
    if match:
        price = float(match.group(1))

    # Extract duration when explicitly mentioned
    duration = None
    match = re.search(
        r"\b(\d+)\s*(days?|weeks?|months?)\b",
        text_lower
    )
    if match:
        duration = match.group(0)

    # Extract dates only when a month is explicitly mentioned
    dates = None
    match = re.search(
        r"\b(january|february|march|april|may|june|july|"
        r"august|september|october|november|december)\b",
        text_lower
    )
    if match:
        dates = match.group(1).title()

    # These fields are not implemented in this stub
    origin_country = None
    needs_review = None

    return LeadFields(
        name=name,
        travelers=travelers,
        dates=dates,
        location=location,
        duration=duration,
        origin_country=origin_country,
        price=price,
        needs_review=needs_review
    )


@app.get("/")
async def home():
    return {"message": "Lead Extraction API is running"}


@app.post("/extract", response_model=ExtractionResponse)
def extract_lead(request: ExtractRequest):
    extracted_data = extract_lead_stub(request.text)

    # Check whether any field was extracted
    extracted_values = extracted_data.model_dump()

    if all(value is None for value in extracted_values.values()):
        return ExtractionResponse(
            status="partial",
            data=extracted_data,
            warnings=["No supported fields could be extracted."]
        )

    return ExtractionResponse(
        status="success",
        data=extracted_data
    )
