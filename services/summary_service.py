from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# --------------------------------
# EXTRACT VIDEO ID
# --------------------------------
def get_video_id(video_url):

    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"shorts/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, video_url)

        if match:
            return match.group(1)

    return None


# --------------------------------
# VIDEO SUMMARY
# --------------------------------
def summarize_video(video_url):

    try:

        # Extract video ID
        video_id = get_video_id(video_url)

        if not video_id:
            print(
                "\nInvalid YouTube video URL.\n"
                "Please paste an actual video link.\n"
            )
            return

        print("\nFetching transcript...\n")

        # Get transcript
        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        transcript_text = " ".join(
            [item.text for item in transcript]
        )

        print("\nGenerating AI mentor summary...\n")

        # Better mentor prompt
        prompt = f"""
You are an expert AI mentor.

A student watched an educational YouTube video.

Your job:
Help the student learn from it.

Transcript:
{transcript_text[:10000]}

Generate output in this EXACT structure:

==================================================
VIDEO SUMMARY
==================================================

1. What This Video Teaches
(2-4 lines summary)

2. Key Learnings
(Bullet points)

3. Important Concepts Explained Simply
(Explain for beginner)

4. Common Mistakes to Avoid
(If relevant)

5. Practice Task
(Give actionable task)

6. What To Learn Next
(Suggest logical next topic)

IMPORTANT:
- Keep beginner friendly
- Make learning practical
- Give useful advice
- Avoid complicated language
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are a world-class learning mentor."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        print("\n" + "=" * 60)
        print("AI LEARNING VIDEO SUMMARY")
        print("=" * 60)

        print(
            response.choices[0]
            .message.content
        )

    except Exception as e:

        print("\nError summarizing video:")
        print(e)