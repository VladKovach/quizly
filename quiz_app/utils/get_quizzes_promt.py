def get_quizzes_promt(transcript):
    return f"""You are a quiz generator. Analyze the transcript below and generate a quiz object based on its content.

    RULES:
    1. Respond ONLY in the same language as the transcript. Do NOT translate.
    2. Return ONLY a valid raw JSON object. No markdown, no code blocks, no explanation — just the JSON.
    3. Each question must have exactly 4 answer options.
    4. The "answer" field is a correct option and must be exactly one the options in "answer_options".
    5. Questions must be based strictly on the transcript content — no outside knowledge.
    6. Questions should vary in difficulty and cover different parts of the transcript.
    7. Exectly numbers of questions - 10.
    7. Avoid trivial or repeated questions.
    8. "title" must be a short headline summarizing the transcript (max 100 characters).
    9. "description" must be a short summary of the transcript content (max 300 characters). Write it as a direct summary of the topic, not as a description about what TRANSCRIPT is, only summary info
    10. NEVER reference "the transcript", "the video", "the speaker", "the author" in any question or answer option.
    11. Write questions as direct knowledge questions — as if from a textbook or exam.
        - BAD:  "What does the transcript say about X?"
        - BAD:  "According to the video, what is X?"
        - GOOD: "What is the correct way to handle X?"
        - GOOD: "Which of the following best describes X?"
    REQUIRED JSON FORMAT:
    {{
    "title": "Short headline about the transcript topic",
    "description": "A brief summary of what the transcript is about, max 300 characters.",
    "questions": [
        {{
        "question_title": "The question text here?",
        "answer_options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "Option A"
        }}
    ]
    }}

    TRANSCRIPT:
    {transcript}

    IMPORTANT: Return ONLY valid JSON. No trailing commas. No extra text outside the JSON block.
    """
