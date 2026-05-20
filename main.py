from groq import Groq
from dotenv import load_dotenv
import os

from services.youtube_service import recommend_videos
from services.summary_service import summarize_video
from services.calendar_service import add_learning_schedule

# --------------------------------
# LOAD ENV VARIABLES
# --------------------------------
load_dotenv()

# --------------------------------
# GROQ CLIENT
# --------------------------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# --------------------------------
# GENERATE ROADMAP
# --------------------------------
def generate_roadmap(
    skill,
    goal,
    level,
    months,
    hours_per_day
):

    prompt = f"""
You are an expert AI Skill Mentor.

Create a HIGHLY PERSONALIZED roadmap.

USER DETAILS:

Skill: {skill}
Goal: {goal}
Current Level: {level}
Duration: {months} months
Daily Study Time: {hours_per_day} hours

IMPORTANT:

1. Understand skill domain automatically.

Examples:
- Gym → Fitness
- Japanese → Language Learning
- Spring Boot → Programming
- Photography → Creative Skill

2. Adapt roadmap using:
- Goal
- Level
- Duration
- Daily study time

3. Goal matters.

Examples:

Gym + muscle gain
→ strength training,
protein,
progressive overload

Gym + weight loss
→ cardio,
fat loss,
diet

Japanese + travel
→ speaking,
travel phrases,
restaurant vocabulary

Spring Boot + job
→ Java,
Spring Core,
REST APIs,
JPA,
Projects,
Interview prep

4. DO NOT GIVE GENERIC ROADMAP.

OUTPUT FORMAT:

1. Skill Domain Identified

2. Personalized Learning Strategy

3. Month-by-Month Roadmap

4. Weekly Focus Areas

5. Daily Study Plan

6. Practice Methods

7. Beginner → Intermediate → Advanced Path

Keep response:
- beginner friendly
- structured
- practical
- meaningful
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are a world-class personalized mentor."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"""
Error generating roadmap.

Reason:
{e}
"""


# --------------------------------
# MAIN FUNCTION
# --------------------------------
def main():

    print("\n===== AI Skill Mentor Agent =====\n")

    # QUESTION 1
    skill = input(
        "What skill do you want to learn? "
    )

    # QUESTION 2
    goal = input(
        "What is your goal? "
        "(Travel / Job / Weight Loss / "
        "Muscle Gain / Project / Fun): "
    )

    # QUESTION 3
    level = input(
        "What is your current level? "
        "(Beginner / Intermediate / Advanced): "
    )

    # QUESTION 4
    months = input(
        "How many months? "
    )

    hours_per_day = input(
        "How many hours per day? "
    )

    # Calendar time
    study_time = input(
        "Preferred study time? "
        "(HH:MM 24-hour format, e.g. 18:00): "
    )

    print("\nGenerating personalized roadmap...\n")

    roadmap = generate_roadmap(
        skill,
        goal,
        level,
        months,
        hours_per_day
    )

    print("\n" + "=" * 60)
    print("YOUR PERSONALIZED LEARNING ROADMAP")
    print("=" * 60)

    print(roadmap)

    print("\n" + "=" * 60)

    # --------------------------------
    # GOOGLE CALENDAR
    # --------------------------------
    calendar_choice = input(
        "\nDo you want to add study sessions "
        "to Google Calendar? (yes/no): "
    )

    if calendar_choice.lower() == "yes":

        add_learning_schedule(
            skill,
            study_time
        )

    # --------------------------------
    # BETTER YOUTUBE RECOMMENDATION
    # --------------------------------
    youtube_query = (
        f"{skill} "
        f"{goal} "
        f"{level} tutorial"
    )

    recommend_videos(
        youtube_query
    )

    # --------------------------------
    # VIDEO SUMMARIZATION
    # --------------------------------
    choice = input(
        "\nDo you want video summarization? "
        "(yes/no): "
    )

    if choice.lower() == "yes":

        video_url = input(
            "\nPaste YouTube video URL: "
        )

        summarize_video(
            video_url
        )


# --------------------------------
# RUN APP
# --------------------------------
if __name__ == "__main__":
    main()