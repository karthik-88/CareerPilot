
import pytest

from app.main import main
from app.tools.job_shortlist import shortlist

@pytest.fixture(autouse=True)
def reset_shortlist():
    shortlist.clear()
    yield
    shortlist.clear()

def run_cli(monkeypatch, capsys, inputs):
    simulated_inputs = iter(inputs)

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(simulated_inputs)
    )

    main()

    return capsys.readouterr().out


# -------------------------------
# MENU TESTS
# -------------------------------

def test_exit_application(monkeypatch, capsys):
    output = run_cli(monkeypatch, capsys, ["6"])

    assert "Thank you for using CareerPilot!" in output


def test_invalid_menu_choice(monkeypatch, capsys):
    output = run_cli(monkeypatch, capsys, ["9", "6"])

    assert "Invalid choice. Please try again." in output
    assert "Thank you for using CareerPilot!" in output


# -------------------------------
# JOB SEARCH TESTS
# -------------------------------

def test_search_matching_jobs(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["1", "Python", "Bengaluru", "6"]
    )

    assert "TechNova" in output
    assert "DevSphere" in output
    assert "Job ID: 101" in output
    assert "Job ID: 104" in output


def test_search_no_matching_jobs(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["1", "Java", "Bengaluru", "6"]
    )

    assert "No matching jobs found." in output


def test_search_invalid_role(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["1", "", "Bengaluru", "6"]
    )

    assert "Role must be a non-empty string" in output


# -------------------------------
# JOB DETAILS TESTS
# -------------------------------

def test_view_valid_job_details(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["2", "101", "6"]
    )

    assert "TechNova" in output
    assert "Python Developer" in output
    assert "Python, FastAPI, SQL" in output


def test_view_nonexistent_job(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["2", "999", "6"]
    )

    assert "Job with ID 999 not found" in output


def test_view_non_numeric_job_id(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["2", "abc", "6"]
    )

    assert "invalid literal for int()" in output


# -------------------------------
# ADD TO SHORTLIST TESTS
# -------------------------------

def test_add_job_to_shortlist(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["3", "101", "6"]
    )

    assert "Job added successfully" in output


def test_add_duplicate_job(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["3", "101", "3", "101", "6"]
    )

    assert "Job added successfully" in output
    assert "Job already shortlisted" in output


def test_add_invalid_job_id(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["3", "abc", "6"]
    )

    assert "invalid literal for int()" in output


# -------------------------------
# VIEW SHORTLIST TESTS
# -------------------------------

def test_view_empty_shortlist(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["4", "6"]
    )

    assert "Your shortlist is empty." in output


def test_view_populated_shortlist(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["3", "101", "4", "6"]
    )

    assert "Job added successfully" in output
    assert "Your Shortlisted Jobs:" in output
    assert "TechNova" in output


# -------------------------------
# REMOVE FROM SHORTLIST TESTS
# -------------------------------

def test_remove_shortlisted_job(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["3", "101", "5", "101", "6"]
    )

    assert "Job added successfully" in output
    assert "Job removed successfully" in output


def test_remove_job_not_in_shortlist(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["5", "102", "6"]
    )

    assert "Job not found in shortlist" in output


def test_remove_invalid_job_id(monkeypatch, capsys):
    output = run_cli(
        monkeypatch, capsys,
        ["5", "abc", "6"]
    )

    assert "invalid literal for int()" in output
