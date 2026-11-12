import pytest
from app.tools.job_details import get_job_details


def test_get_existing_job():
    result = get_job_details(102)

    assert result["id"] == 102
    assert result["role"] == "AI Engineer"
    assert result["company"] == "NeuralWorks"
def test_invalid_string_id():
    with pytest.raises(ValueError, match="positive integer"):
        get_job_details("hello")


def test_invalid_none_id():
    with pytest.raises(ValueError, match="positive integer"):
        get_job_details(None)


def test_invalid_zero_id():
    with pytest.raises(ValueError, match="positive integer"):
        get_job_details(0)


def test_nonexistent_job_id():
    with pytest.raises(ValueError, match="not found"):
        get_job_details(999)