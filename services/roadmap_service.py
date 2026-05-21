from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


def generate_roadmap(
    skill,
    goal,
    level,
    months,
    hours_per_day
):

    prompt = f"""
You are an expert AI mentor.

Generate a PERSONALIZED
learning roadmap.

Skill:
{skill}

Goal:
{goal}

Level:
{level}

Duration:
{months} months

Daily Time:
{hours_per_day} hours

IMPORTANT:

1. Detect domain automatically.

Examples:
Gym → Fitness
Japanese → Language
Spring Boot → Programming
Cooking → Lifestyle

2. DO NOT GIVE
GENERIC ROADMAP.

3. Adapt roadmap
based on:
- goal
- level
- duration
- daily hours

Output format:

1. Skill Domain
2. Personalized Strategy
3. Month-by-Month Plan
4. Weekly Focus
5. Daily Plan
6. Practice Methods
7. Long-Term Advice

Make it practical
and domain specific.
"""

    try:

        response = (
            client.chat.completions.create(
                model=
                "llama-3.3-70b-versatile",

                messages=[
                    {
                        "role":
                        "system",

                        "content":
                        "You are a "
                        "world-class "
                        "mentor."
                    },
                    {
                        "role":
                        "user",

                        "content":
                        prompt
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

        return (
            f"Roadmap error:\n{e}"
        )