
from types import SimpleNamespace

import pytest

from app.llm import gemini_client


MODEL = "gemini-3.5-flash-lite"


def test_generate_response(monkeypatch):
    # Fake Gemini response
    fake_response = SimpleNamespace(
        text="An AI agent performs tasks autonomously."
    )

    # Fake Gemini client
    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=lambda **kwargs: fake_response
        )
    )

    monkeypatch.setattr(
        gemini_client,
        "_get_client",
        lambda: fake_client
    )

    result = gemini_client.generate_response("Explain AI agents")

    assert result == "An AI agent performs tasks autonomously."


def test_generate_response_uses_correct_arguments(monkeypatch):
    received_arguments = {}

    def fake_generate_content(**kwargs):
        received_arguments.update(kwargs)
        return SimpleNamespace(text="Test response")

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=fake_generate_content
        )
    )

    monkeypatch.setattr(
        gemini_client,
        "_get_client",
        lambda: fake_client
    )

    gemini_client.generate_response("Hello Gemini")

    assert received_arguments["model"] == MODEL
    assert received_arguments["contents"] == "Hello Gemini"


def test_stream_response(monkeypatch):
    # Simulate Gemini sending three chunks
    fake_chunks = [
        SimpleNamespace(text="Hello "),
        SimpleNamespace(text="Career"),
        SimpleNamespace(text="Pilot!")
    ]

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content_stream=lambda **kwargs: iter(fake_chunks)
        )
    )

    monkeypatch.setattr(
        gemini_client,
        "_get_client",
        lambda: fake_client
    )

    result = list(gemini_client.stream_response("Say hello"))

    assert result == ["Hello ", "Career", "Pilot!"]


def test_stream_response_ignores_empty_chunks(monkeypatch):
    fake_chunks = [
        SimpleNamespace(text="Hello "),
        SimpleNamespace(text=None),
        SimpleNamespace(text=""),
        SimpleNamespace(text="World!")
    ]

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content_stream=lambda **kwargs: iter(fake_chunks)
        )
    )

    monkeypatch.setattr(
        gemini_client,
        "_get_client",
        lambda: fake_client
    )

    result = list(gemini_client.stream_response("Say hello"))

    assert result == ["Hello ", "World!"]


def test_generate_response_propagates_api_error(monkeypatch):
    def fake_generate_content(**kwargs):
        raise RuntimeError("Gemini service unavailable")

    fake_client = SimpleNamespace(
        models=SimpleNamespace(
            generate_content=fake_generate_content
        )
    )

    monkeypatch.setattr(
        gemini_client,
        "_get_client",
        lambda: fake_client
    )

    with pytest.raises(RuntimeError, match="Gemini service unavailable"):
        gemini_client.generate_response("Hello")
