
from types import SimpleNamespace

import pytest

from app.llm import gemini_client
from app.llm.prompts import CAREERPILOT_SYSTEM_INSTRUCTION


def test_generate_response(monkeypatch):
    """Test that Gemini response text is returned."""

    fake_response = SimpleNamespace(text="Hello from Gemini!")

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda **kwargs: fake_response
        )
    )

    monkeypatch.setattr(
        gemini_client, "_get_client", lambda: fake_client
    )

    result = gemini_client.generate_response("Hello")

    assert result == "Hello from Gemini!"


def test_generate_response_uses_correct_arguments(monkeypatch):
    """Test model, prompt and system instruction arguments."""

    captured_arguments = {}

    def fake_generate_content(**kwargs):
        captured_arguments.update(kwargs)
        return SimpleNamespace(text="Test response")

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=fake_generate_content
        )
    )

    monkeypatch.setattr(
        gemini_client, "_get_client", lambda: fake_client
    )

    gemini_client.generate_response("Find Python jobs")

    assert captured_arguments["model"] == "gemini-3.5-flash-lite"
    assert captured_arguments["contents"] == "Find Python jobs"
    assert (
        captured_arguments["config"].system_instruction
        == CAREERPILOT_SYSTEM_INSTRUCTION
    )


def test_stream_response(monkeypatch):
    """Test that streaming responses are yielded correctly."""

    fake_chunks = [
        SimpleNamespace(text="Hello "),
        SimpleNamespace(text="from "),
        SimpleNamespace(text="Gemini!")
    ]

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content_stream=lambda **kwargs: fake_chunks
        )
    )

    monkeypatch.setattr(
        gemini_client, "_get_client", lambda: fake_client
    )

    result = list(gemini_client.stream_response("Hello"))

    assert result == ["Hello ", "from ", "Gemini!"]


def test_stream_response_uses_correct_arguments(monkeypatch):
    """Test model, prompt and system instruction for streaming."""

    captured_arguments = {}

    def fake_generate_content_stream(**kwargs):
        captured_arguments.update(kwargs)

        return iter([
            SimpleNamespace(text="CareerPilot response")
        ])

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content_stream=fake_generate_content_stream
        )
    )

    monkeypatch.setattr(
        gemini_client, "_get_client", lambda: fake_client
    )

    result = list(
        gemini_client.stream_response("Find AI Engineer jobs")
    )

    assert result == ["CareerPilot response"]
    assert captured_arguments["model"] == "gemini-3.5-flash-lite"
    assert captured_arguments["contents"] == "Find AI Engineer jobs"
    assert (
        captured_arguments["config"].system_instruction
        == CAREERPILOT_SYSTEM_INSTRUCTION
    )


def test_stream_response_ignores_empty_chunks(monkeypatch):
    """Test that empty streaming chunks are ignored."""

    fake_chunks = [
        SimpleNamespace(text="Hello "),
        SimpleNamespace(text=None),
        SimpleNamespace(text=""),
        SimpleNamespace(text="Gemini!")
    ]

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content_stream=lambda **kwargs: fake_chunks
        )
    )

    monkeypatch.setattr(
        gemini_client, "_get_client", lambda: fake_client
    )

    result = list(gemini_client.stream_response("Hello"))

    assert result == ["Hello ", "Gemini!"]


def test_generate_response_propagates_api_error(monkeypatch):
    """Test that Gemini API errors are propagated."""

    def fake_generate_content(**kwargs):
        raise RuntimeError("Gemini API error")

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=fake_generate_content
        )
    )

    monkeypatch.setattr(
        gemini_client, "_get_client", lambda: fake_client
    )

    with pytest.raises(RuntimeError, match="Gemini API error"):
        gemini_client.generate_response("Hello")
