
import pytest

from app.tools.job_shortlist import (
    add_to_shortlist,
    view_shortlist,
    remove_from_shortlist,
    shortlist
)


# Reset the shortlist before and after every test
@pytest.fixture(autouse=True)
def reset_shortlist():
    shortlist.clear()
    yield
    shortlist.clear()


# 1. Test adding a valid job
def test_add_valid_job():
    result = add_to_shortlist(101)

    assert result == "Job added successfully"
    assert shortlist == [101]


# 2. Test preventing duplicate jobs
def test_prevent_duplicate_job():
    add_to_shortlist(101)

    result = add_to_shortlist(101)

    assert result == "Job already shortlisted"
    assert shortlist == [101]


# 3. Test adding a non-existent job
def test_add_nonexistent_job():
    with pytest.raises(ValueError, match="not found"):
        add_to_shortlist(999)

    assert shortlist == []


# 4. Test viewing an empty shortlist
def test_view_empty_shortlist():
    result = view_shortlist()

    assert result == []


# 5. Test viewing shortlisted jobs
def test_view_shortlist():
    add_to_shortlist(101)
    add_to_shortlist(104)

    result = view_shortlist()

    assert len(result) == 2
    assert result[0]["id"] == 101
    assert result[1]["id"] == 104
    assert result[0]["role"] == "Python Developer"


# 6. Test removing an existing job
def test_remove_existing_job():
    add_to_shortlist(101)
    add_to_shortlist(104)

    result = remove_from_shortlist(104)

    assert result == "Job removed successfully"
    assert shortlist == [101]


# 7. Test removing a job that isn't shortlisted
def test_remove_job_not_in_shortlist():
    add_to_shortlist(101)

    result = remove_from_shortlist(102)

    assert result == "Job not found in shortlist"
    assert shortlist == [101]

def test_add_invalid_job_id():
    with pytest.raises(ValueError, match="positive integer"):
        add_to_shortlist("hello")


def test_remove_invalid_job_id():
    with pytest.raises(ValueError, match="positive integer"):
        remove_from_shortlist("hello")


def test_remove_nonexistent_dataset_job():
    with pytest.raises(ValueError, match="not found"):
        remove_from_shortlist(999)