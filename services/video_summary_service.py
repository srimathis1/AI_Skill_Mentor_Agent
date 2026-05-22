from youtube_transcript_api import (
    YouTubeTranscriptApi
)

from groq import Groq
from dotenv import load_dotenv

import os
import re

load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


# ==========================
# EXTRACT VIDEO ID
# ==========================
def extract_video_id(
    url
):

    pattern = (
        r"(?:v=|\/)"
        r"([0-9A-Za-z_-]{11})"
    )

    match = re.search(
        pattern,
        url
    )

    if match:
        return (
            match.group(1)
        )

    raise Exception(
        "Invalid YouTube URL"
    )


# ==========================
# SUMMARIZE VIDEO
# ==========================
def summarize_video(
    youtube_url
):

    try:

        video_id = (
            extract_video_id(
                youtube_url
            )
        )

        # FIXED VERSION
        transcript_list = (
            YouTubeTranscriptApi()
            .fetch(video_id)
        )

        transcript_text = " ".join(

            item.text
            for item
            in transcript_list
        )

        response = (
            client.chat.completions.create(
                model=
                "llama-3.3-70b-versatile",

                messages=[

                    {
                        "role":
                        "system",

                        "content":
                        """
You summarize
educational videos.

Give:

1. Key concepts
2. Important takeaways
3. Learning notes
4. Action items

Keep summary clear
and structured.
"""
                    },

                    {
                        "role":
                        "user",

                        "content":
                        transcript_text[
                            :12000
                        ]
                    }
                ]
            )
        )

        return (
            response
            .choices[0]
            .message.content
        )

    except Exception as e:

        raise Exception(
            f"Could not summarize "
            f"video: {e}"
        )