
from google import genai

client = None


def _get_client():
    global client

    if client is None:
        client = genai.Client()

    return client


def generate_response(prompt):

    response = _get_client().models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


def stream_response(prompt):

    response_stream = _get_client().models.generate_content_stream(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    for chunk in response_stream:
        if chunk.text:
            yield chunk.text
