
import pytest
from pydantic import ValidationError
from main import ExtractRequest, LeadFields


def test_reject_overlong_text():
    with pytest.raises(ValidationError):
        ExtractRequest(text="a" * 2001)


def test_reject_invalid_quantities():
    with pytest.raises(ValidationError):
        LeadFields(travelers=0)

    with pytest.raises(ValidationError):
        LeadFields(price=-100)


def test_missing_fields_are_null():
    lead = LeadFields()

    assert lead.travelers is None
    assert lead.dates is None
    assert lead.location is None
    assert lead.duration is None
    assert lead.origin_country is None
    assert lead.price is None
    assert lead.needs_review is None
    
@app.post("/extract", response_model=ExtractionResponse)
def extract_lead(request: ExtractRequest):
    # Right now it just returns an empty LeadFields() object!
    return ExtractionResponse(
        status="success",
        data=LeadFields()
    )

