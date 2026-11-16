
import time

from app.llm.gemini_client import stream_response

prompt = "Explain AI agents in 3 sentences."

start_time = time.perf_counter()
first_chunk_time = None

print("\nGemini response:")

try:
    for chunk in stream_response(prompt):

        if first_chunk_time is None:
            first_chunk_time = time.perf_counter()

        print(chunk, end="", flush=True)

    end_time = time.perf_counter()

    print("\n\nPerformance:")

    if first_chunk_time is not None:
        print(
            f"Time to first chunk: "
            f"{first_chunk_time - start_time:.2f} seconds"
        )

    print(f"Total response time: {end_time - start_time:.2f} seconds")

except Exception as error:
    print(f"\nGemini API error: {error}")
