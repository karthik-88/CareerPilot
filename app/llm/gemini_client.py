
from google import genai
from google.genai import types
from app.llm.prompts import CAREERPILOT_SYSTEM_INSTRUCTION

client = None


def _get_client():
    global client

    if client is None:
        client = genai.Client()

    return client


def generate_response(prompt):

    response = _get_client().models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=CAREERPILOT_SYSTEM_INSTRUCTION
        )
    )

    return response.text


def stream_response(prompt):

    response_stream = _get_client().models.generate_content_stream(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=CAREERPILOT_SYSTEM_INSTRUCTION
        )
    )

    for chunk in response_stream:
        if chunk.text:
            yield chunk.text

