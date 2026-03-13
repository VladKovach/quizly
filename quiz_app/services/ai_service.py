import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

from quiz_app.utils import get_quizzes_promt

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELS = [
    "gemini-2.5-pro",  # 100 req/day
    "gemini-2.5-flash",  # 500 req/day
    "gemini-2.0-flash",  # 1000 req/day
]


def generate_quizzes(transcript: str):
    prompt = get_quizzes_promt(transcript)

    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            return response.text
        except ClientError as e:
            if e.code == 429:
                continue
            return {
                "error": True,
                "message": "Unknown error. Try again later.",
            }

    return {
        "error": True,
        "message": "All Gemini models are rate limited. Try again later.",
    }
