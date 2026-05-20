from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


def add_learning_schedule(skill, preferred_time):

    try:

        creds = None

        # safer path
        BASE_DIR = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        token_path = os.path.join(
            BASE_DIR,
            "token.json"
        )

        credentials_path = os.path.join(
            BASE_DIR,
            "credentials.json"
        )

        if os.path.exists(token_path):

            creds = (
                Credentials
                .from_authorized_user_file(
                    token_path,
                    SCOPES
                )
            )

        if not creds or not creds.valid:

            if (
                creds
                and creds.expired
                and creds.refresh_token
            ):
                creds.refresh(
                    Request()
                )

            else:

                flow = (
                    InstalledAppFlow
                    .from_client_secrets_file(
                        credentials_path,
                        SCOPES
                    )
                )

                creds = (
                    flow.run_local_server(
                        port=0
                    )
                )

            with open(
                token_path,
                "w"
            ) as token:

                token.write(
                    creds.to_json()
                )

        service = build(
            "calendar",
            "v3",
            credentials=creds
        )

        # Domain aware naming
        fitness_keywords = [
            "gym",
            "fitness",
            "workout",
            "weight loss",
            "muscle gain"
        ]

        if skill.lower() in fitness_keywords:
            session_name = (
                f"{skill} Workout"
            )
        else:
            session_name = (
                f"{skill} Learning"
            )

        for i in range(7):

            start_date = (
                datetime.datetime.now()
                + datetime.timedelta(
                    days=i + 1
                )
            )

            time_obj = (
                datetime.datetime.strptime(
                    preferred_time,
                    "%H:%M"
                )
            )

            start_datetime = (
                start_date.replace(
                    hour=time_obj.hour,
                    minute=time_obj.minute,
                    second=0
                )
            )

            end_datetime = (
                start_datetime
                + datetime.timedelta(
                    hours=1
                )
            )

            event = {
                "summary":
                session_name,

                "description":
                f"AI Skill Mentor "
                f"- {skill}",

                "start": {
                    "dateTime":
                    start_datetime.isoformat(),

                    "timeZone":
                    "Asia/Kolkata",
                },

                "end": {
                    "dateTime":
                    end_datetime.isoformat(),

                    "timeZone":
                    "Asia/Kolkata",
                },

                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {
                            "method":
                            "popup",

                            "minutes":
                            30
                        }
                    ]
                }
            }

            service.events().insert(
                calendarId="primary",
                body=event
            ).execute()

        print(
            "\nCalendar events added successfully!\n"
        )

    except Exception as e:

        print(
            f"\nCalendar Error: {e}"
        )

        print(
            "\nContinuing app...\n"
        )