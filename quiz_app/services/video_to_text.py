import re

from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)


def get_video_transcript(youtube_url):
    video_id = re.search(r"(?:v=|youtu\.be/)([^&?/]+)", youtube_url).group(1)

    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)

        try:
            transcript = transcript_list.find_transcript(["en"])
        except NoTranscriptFound:
            transcript = transcript_list.find_generated_transcript(
                [t.language_code for t in transcript_list]
            )

        fetched = transcript.fetch()
        return " ".join([snippet.text for snippet in fetched.snippets])

    except (TranscriptsDisabled, NoTranscriptFound):
        return None
