import time

from app.llm.gemini_client import generate_response

prompt = "Explain AI agents in 2 sentences."

start_time = time.perf_counter()

try:
    response = generate_response(prompt)

    end_time = time.perf_counter()

    print("\nGemini response:")
    print(response)

    print(f"\nResponse time: {end_time - start_time:.2f} seconds")

except Exception as error:
    print(f"Gemini API error: {error}")