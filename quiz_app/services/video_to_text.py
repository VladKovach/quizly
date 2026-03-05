import glob
import json
import os

import yt_dlp


def get_video_transcript(youtube_url: str) -> dict:
    """
    Receives a YouTube URL, returns json.
    """

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "outtmpl": "/temporary/%(title)s.%(ext)s",
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)

        # ℹ️ ydl.sanitize_info makes the info json-serializable
        # print("json.dump = ", json.dumps(ydl.sanitize_info(info)))


#     # find the downloaded .vtt subtitle file
#     vtt_files = glob.glob(f"{output_dir}/*.vtt")
#     if not vtt_files:
#         return {
#             "title": title,
#             "text": None,
#             "error": "No subtitles available for this video",
#         }

#     transcript_text = _parse_vtt(vtt_files[0])

#     # cleanup
#     for f in vtt_files:
#         os.remove(f)

#     return {"title": title, "text": transcript_text}


# def _parse_vtt(filepath: str) -> str:
#     """
#     Parses a .vtt subtitle file and returns clean plain text.
#     Removes timestamps, tags, and duplicate lines.
#     """
#     import re

#     with open(filepath, "r", encoding="utf-8") as f:
#         content = f.read()

#     # remove WEBVTT header and timestamp lines
#     lines = content.split("\n")
#     clean_lines = []
#     seen = set()

#     for line in lines:
#         line = line.strip()
#         # skip empty, timestamp lines, WEBVTT header
#         if (
#             not line
#             or "-->" in line
#             or line.startswith("WEBVTT")
#             or line.isdigit()
#         ):
#             continue
#         # remove HTML tags like <00:00:01.000>, <c>, </c>
#         line = re.sub(r"<[^>]+>", "", line)
#         # avoid duplicate lines (auto-subs repeat a lot)
#         if line not in seen:
#             seen.add(line)
#             clean_lines.append(line)

#     return " ".join(clean_lines)
