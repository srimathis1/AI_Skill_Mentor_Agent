import smtplib
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


def send_weekly_email(
    receiver_email,
    skill,
    roadmap
):

    try:

        sender_email = os.getenv(
            "EMAIL_USER"
        )

        sender_password = os.getenv(
            "EMAIL_PASSWORD"
        )

        subject = (
            f"Your Weekly "
            f"{skill} Learning Report"
        )

        body = f"""
Hello,

Here is your weekly progress
report for {skill}.

Recommended Focus:
- Stay consistent
- Follow roadmap
- Practice daily

Roadmap Reminder:
{roadmap[:500]}

Motivation:
Small progress every day
creates big results 🔥

AI Skill Mentor
"""

        msg = MIMEMultipart()

        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(
            MIMEText(
                body,
                "plain"
            )
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.sendmail(
            sender_email,
            receiver_email,
            msg.as_string()
        )

        server.quit()

        print(
            "\nWeekly email sent successfully!\n"
        )

    except Exception as e:

        print(
            "\nEmail Error:"
        )

        print(e)