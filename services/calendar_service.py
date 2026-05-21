from __future__ import print_function

import os
from datetime import datetime, timedelta
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# ----------------------------
# GOOGLE CALENDAR SCOPE
# ----------------------------
SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


# ----------------------------
# ADD LEARNING SCHEDULE
# ----------------------------
def add_learning_schedule(
    skill,
    preferred_time
):

    try:

        creds = None

        # ----------------------------
        # PROJECT PATHS
        # ----------------------------
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

        # ----------------------------
        # LOAD TOKEN
        # ----------------------------
        if os.path.exists(
            token_path
        ):

            creds = (
                Credentials
                .from_authorized_user_file(
                    token_path,
                    SCOPES
                )
            )

        # ----------------------------
        # LOGIN IF NEEDED
        # ----------------------------
        if (
            not creds
            or not creds.valid
        ):

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

        # ----------------------------
        # CALENDAR SERVICE
        # ----------------------------
        service = build(
            "calendar",
            "v3",
            credentials=creds
        )

        # ----------------------------
        # SMART EVENT TITLE
        # ----------------------------
        fitness_keywords = [
            "gym",
            "fitness",
            "workout",
            "muscle gain",
            "weight loss"
        ]

        if (
            skill.lower()
            in fitness_keywords
        ):

            event_title = (
                f"{skill.title()} Workout"
            )

        else:

            event_title = (
                f"{skill.title()} Learning"
            )

        # ----------------------------
        # FORCE INDIA TIMEZONE
        # ----------------------------
        india_tz = pytz.timezone(
            "Asia/Kolkata"
        )

        # Parse user time
        hour, minute = map(
            int,
            preferred_time.split(":")
        )

        today = datetime.now(
            india_tz
        )

        start_datetime = india_tz.localize(
            datetime(
                today.year,
                today.month,
                today.day,
                hour,
                minute,
                0
            )
        )

        # If today's time passed
        if (
            start_datetime
            < today
        ):
            start_datetime += timedelta(
                days=1
            )

        end_datetime = (
            start_datetime
            + timedelta(hours=1)
        )

        print(
            "\nAdding calendar event...\n"
        )

        # ----------------------------
        # CREATE EVENT
        # ----------------------------
        event = {

            "summary":
            event_title,

            "description":
            (
                f"AI Skill Mentor\n"
                f"Skill: {skill}"
            ),

            "start": {

                "dateTime":
                start_datetime.isoformat(),

                "timeZone":
                "Asia/Kolkata"
            },

            "end": {

                "dateTime":
                end_datetime.isoformat(),

                "timeZone":
                "Asia/Kolkata"
            },

            # recurring 30 days
            "recurrence": [
                "RRULE:FREQ=DAILY;COUNT=30"
            ],

            "reminders": {

                "useDefault":
                False,

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

        created_event = (
            service.events()
            .insert(
                calendarId="primary",
                body=event
            )
            .execute()
        )

        print(
            f"\nAdded successfully "
            f"at {preferred_time} IST"
        )

        print(
            created_event.get(
                "htmlLink"
            )
        )

        print(
            "\nCalendar event "
            "added successfully!\n"
        )

    except Exception as e:

        print(
            f"\nCalendar Error: {e}"
        )

        print(
            "\nContinuing app...\n"
        )