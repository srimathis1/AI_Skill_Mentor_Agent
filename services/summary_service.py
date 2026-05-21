import re

from youtube_transcript_api import (
    YouTubeTranscriptApi
)


def get_video_id(
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
        return match.group(1)

    return None


def summarize_video(
    video_url
):

    try:

        video_id = (
            get_video_id(
                video_url
            )
        )

        if not video_id:

            return (
                "Invalid "
                "YouTube URL."
            )

        transcript = (
            YouTubeTranscriptApi
            .get_transcript(
                video_id
            )
        )

        text = " ".join(

            [
                entry["text"]

                for entry
                in transcript
            ]
        )

        return (
            text[:1500]
            + "..."
        )

    except Exception as e:

        return (
            f"Summary error:\n{e}"
        )