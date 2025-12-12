from google import genai
from google.genai import types

client = genai.Client(api_key=API_KEY)


def request_gemini(contents, temperature, maxOutputTokens):
    model_name = "gemini-2.5-flash"

    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=temperature, max_output_tokens=maxOutputTokens
        ),
    )

    print(response)

    response_object = {
        "response": response.text,
        "model": model_name,
        "time_taken": 1.23,
    }

    return response_object
