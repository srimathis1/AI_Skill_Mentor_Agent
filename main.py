from groq import Groq
from dotenv import load_dotenv
import os

from services.youtube_service import recommend_videos
from services.video_summary_service import summarize_video
from services.calendar_service import add_learning_schedule
from services.email_service import send_weekly_email

# --------------------------------
# LOAD ENV
# --------------------------------
load_dotenv()

# --------------------------------
# GROQ CLIENT
# --------------------------------
client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
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

Generate a HIGHLY PERSONALIZED roadmap.

USER DETAILS:

Skill: {skill}
Goal: {goal}
Level: {level}
Duration: {months} months
Daily Time: {hours_per_day} hours

IMPORTANT:

1. Detect domain automatically.

Examples:
- Gym → Fitness
- Japanese → Language
- Spring Boot → Programming
- Dancing → Creative Skill
- Cooking → Lifestyle

2. DO NOT GIVE GENERIC ROADMAP.

3. Adapt roadmap based on:
- Goal
- Level
- Time available
- Duration

4. Give SPECIFIC learning path.

Examples:

Gym + muscle gain:
- workout split
- protein intake
- progressive overload
- recovery

Japanese + fun:
- anime vocabulary
- conversation
- speaking
- listening

Spring Boot + job:
- Java
- Spring Core
- REST APIs
- JPA
- Security
- Projects

Output format:

1. Skill Domain
2. Personalized Strategy
3. Month-by-Month Roadmap
4. Weekly Focus
5. Daily Plan
6. Practice Methods
7. Long-Term Progression

Keep it:
- practical
- beginner friendly
- domain specific
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
            f"\nRoadmap "
            f"generation error:\n{e}"
        )


# --------------------------------
# MAIN
# --------------------------------
def main():

    print(
        "\n===== "
        "AI Skill Mentor "
        "Agent =====\n"
    )

    # -------------------------
    # USER INPUT
    # -------------------------
    skill = input(
        "What skill do "
        "you want to learn? "
    )

    goal = input(
        "What is your goal? "
        "(Job/Travel/"
        "Fun/Muscle Gain/"
        "Weight Loss/etc): "
    )

    level = input(
        "Current level? "
        "(Beginner/"
        "Intermediate/"
        "Advanced): "
    )

    months = input(
        "How many months? "
    )

    hours_per_day = input(
        "How many hours "
        "per day? "
    )

    preferred_time = input(
        "Preferred schedule "
        "time? "
        "(HH:MM format): "
    )

    print(
        "\nGenerating "
        "personalized roadmap...\n"
    )

    roadmap = (
        generate_roadmap(
            skill,
            goal,
            level,
            months,
            hours_per_day
        )
    )

    # -------------------------
    # ROADMAP OUTPUT
    # -------------------------
    print(
        "\n" + "=" * 60
    )

    print(
        "YOUR PERSONALIZED "
        "LEARNING ROADMAP"
    )

    print(
        "=" * 60
    )

    print(roadmap)

    print(
        "\n" + "=" * 60
    )

    # -------------------------
    # CALENDAR
    # -------------------------
    calendar_choice = input(
        "\nDo you want to "
        "add study sessions "
        "to Google Calendar? "
        "(yes/no): "
    )

    if (
        calendar_choice.lower()
        == "yes"
    ):

        add_learning_schedule(
            skill,
            preferred_time
        )

    # -------------------------
    # EMAIL REPORT
    # -------------------------
    email_choice = input(
        "\nDo you want "
        "weekly progress "
        "emails? "
        "(yes/no): "
    )

    if (
        email_choice.lower()
        == "yes"
    ):

        receiver_email = input(
            "Enter email: "
        )

        send_weekly_email(
            receiver_email,
            skill,
            roadmap
        )

    # -------------------------
    # YOUTUBE
    # -------------------------
    print(
        "\n===== "
        "RECOMMENDED "
        "YOUTUBE VIDEOS "
        "=====\n"
    )

    youtube_query = (
        f"{skill} "
        f"{goal} "
        f"{level} tutorial"
    )

    recommend_videos(
        youtube_query
    )

    # -------------------------
    # VIDEO SUMMARY
    # -------------------------
    summary_choice = input(
        "\nDo you want "
        "video summarization? "
        "(yes/no): "
    )

    if (
        summary_choice.lower()
        == "yes"
    ):

        video_url = input(
            "\nPaste "
            "YouTube URL: "
        )

        summarize_video(
            video_url
        )

    print(
        "\nThanks for using "
        "AI Skill Mentor!"
    )


# --------------------------------
# RUN APP
# --------------------------------
if __name__ == "__main__":
    main()