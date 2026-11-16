
from google import genai

client = genai.Client()


def generate_response(prompt):

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


def stream_response(prompt):

    response_stream = client.models.generate_content_stream(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    for chunk in response_stream:
        if chunk.text:
            yield chunk.text
