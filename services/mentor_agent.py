import os
import json
import re

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from typing import Dict, Any

load_dotenv()

# ==================================
# GROQ
# ==================================
client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


# ==================================
# MODEL
# ==================================
class UserPlan(
    BaseModel):

    skill: str
    goal: str
    duration_months: int
    daily_hours: int
    preferred_time: str
    roadmap: str


# ==================================
# CLEAN JSON
# ==================================
def clean_json(
    text
):

    text = re.sub(
        r"```json",
        "",
        text
    )

    text = re.sub(
        r"```",
        "",
        text
    )

    text = text.strip()

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:
        text = match.group()

    return text


# ==================================
# STEP 1
# EXTRACT DETAILS
# ==================================
def extract_details(
    user_prompt
):

    prompt = f"""
Extract ONLY these fields.

Return ONLY JSON.

{{
"skill":"",
"goal":"",
"duration_months":0,
"daily_hours":0,
"preferred_time":"20:00"
}}

USER:
{user_prompt}
"""

    response = (
        client.chat.completions.create(
            model=
            "llama-3.3-70b-versatile",

            temperature=0,

            messages=[
                {
                    "role":
                    "system",

                    "content":
                    "Return valid JSON only."
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

    result = (
        response
        .choices[0]
        .message.content
    )

    cleaned = clean_json(
        result
    )

    return json.loads(
        cleaned
    )


# ==================================
# STEP 2
# GENERATE ROADMAP
# ==================================
def generate_roadmap(
    details
):

    prompt = f"""
Create ONE complete
personalized roadmap.

Skill:
{details["skill"]}

Goal:
{details["goal"]}

Duration:
{details["duration_months"]} months

Study Hours:
{details["daily_hours"]}

Include:

1. Beginner phase
2. Intermediate phase
3. Advanced phase
4. Weekly strategy
5. Practice ideas
6. Projects
7. Interview/job prep
8. Mistakes to avoid

NO DUPLICATION.
"""

    response = (
        client.chat.completions.create(
            model=
            "llama-3.3-70b-versatile",

            temperature=0.3,

            messages=[
                {
                    "role":
                    "system",

                    "content":
                    "You are an expert mentor."
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


# ==================================
# MAIN
# ==================================
def generate_learning_plan(
    user_prompt
):

    details = extract_details(
        user_prompt
    )

    roadmap = generate_roadmap(
        details
    )

    details[
        "roadmap"
    ] = roadmap

    plan = UserPlan(
        **details
    )

    return plan