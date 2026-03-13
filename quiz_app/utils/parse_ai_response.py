import json
import re


def parse_ai_response(raw: str) -> list:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"```json|```", "", cleaned).strip()

    # Remove trailing commas before ] or }
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

    return json.loads(cleaned)
