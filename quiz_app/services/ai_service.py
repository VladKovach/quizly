import json
import os
import re

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELS = [
    "gemini-2.5-pro",  # 100 req/day
    "gemini-2.5-flash",  # 500 req/day
    "gemini-2.0-flash",  # 1000 req/day
]


def generate_quizzes(transcript: str):
    prompt = f"""You are a quiz generator. Analyze the transcript below and generate a quiz object based on its content.

    RULES:
    1. Respond ONLY in the same language as the transcript. Do NOT translate.
    2. Return ONLY a valid raw JSON object. No markdown, no code blocks, no explanation — just the JSON.
    3. Each question must have exactly 4 answer options.
    4. The "answer" field must be the index (0, 1, 2, or 3) of the correct option in "answer_options".
    5. Questions must be based strictly on the transcript content — no outside knowledge.
    6. Questions should vary in difficulty and cover different parts of the transcript.
    7. Avoid trivial or repeated questions.
    8. "title" must be a short headline summarizing the transcript (max 100 characters).
    9. "description" must be a short summary of the transcript content (max 400 characters). Write it as a direct summary of the topic, not as a description about what TRANSCRIPT is, only summary info

    REQUIRED JSON FORMAT:
    {{
    "title": "Short headline about the transcript topic",
    "description": "A brief summary of what the transcript is about, max 400 characters.",
    "questions": [
        {{
        "question_title": "The question text here?",
        "answer_options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": 0
        }}
    ]
    }}

    TRANSCRIPT:
    {transcript}

    IMPORTANT: Return ONLY valid JSON. No trailing commas. No extra text outside the JSON block.
    """

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


def parse_ai_responce(raw: str) -> list:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"```json|```", "", cleaned).strip()

    # Remove trailing commas before ] or }
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

    return json.loads(cleaned)
