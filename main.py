import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# OpenRouter client
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

print("\n===== AI Skill Mentor Agent =====\n")

goal = input("What skill do you want to learn? ")
duration = input("How many months? ")
daily_time = input("How many hours daily? ")

prompt = f"""
You are an AI Skill Mentor.

User wants to learn:
Skill: {goal}
Duration: {duration} months
Daily study time: {daily_time} hours

Generate:
1. Weekly roadmap
2. Beginner strategy
3. Daily learning plan
4. Recommended learning order

Keep response structured and beginner friendly.
"""

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\n===== YOUR ROADMAP =====\n")
    print(response.choices[0].message.content)

except Exception as e:
    print("Error:", e)