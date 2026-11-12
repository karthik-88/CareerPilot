
import pytest
from app.tools.job_search import search_jobs


def test_python_jobs_in_bengaluru():
    results = search_jobs("Python", "Bengaluru")

    assert len(results) == 2
    assert results[0]["id"] == 101
    assert results[1]["id"] == 104


def test_empty_role():
    with pytest.raises(ValueError):
        search_jobs("", "Bengaluru")


def test_empty_location():
    with pytest.raises(ValueError):
        search_jobs("Python", "")


def test_invalid_role_type():
    with pytest.raises(ValueError):
        search_jobs(None, "Bengaluru")


def test_invalid_location_type():
    with pytest.raises(ValueError):
        search_jobs("Python", None)


def test_no_matching_jobs():
    results = search_jobs("Python", "Chennai")

    assert results == []


def test_case_insensitive_search():
    results = search_jobs("python", "bengaluru")

    assert len(results) == 2
    
def test_whitespace_role():
    with pytest.raises(ValueError):
        search_jobs("   ", "Bengaluru")


def test_whitespace_location():
    with pytest.raises(ValueError):
        search_jobs("Python", "   ")
