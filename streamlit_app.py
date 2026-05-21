import streamlit as st
from streamlit_option_menu import option_menu
import json
import os

from services.roadmap_service import (
    generate_roadmap
)

from services.youtube_service import (
    recommend_videos
)

from services.summary_service import (
    summarize_video
)

from services.calendar_service import (
    add_learning_schedule
)

from services.email_service import (
    send_weekly_email
)

from services.chat_service import (
    save_chat,
    load_chat
)


# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="AI Skill Mentor",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------
# STORAGE
# -----------------------------------
if not os.path.exists(
    "storage"
):
    os.makedirs(
        "storage"
    )

if not os.path.exists(
    "storage/user.json"
):
    with open(
        "storage/user.json",
        "w"
    ) as f:
        json.dump(
            {},
            f
        )


# -----------------------------------
# HEADER
# -----------------------------------
st.markdown(
    """
    <h1 style='text-align:center;
    color:#4F46E5;'>
    🚀 AI Skill Mentor
    </h1>

    <h4 style='text-align:center;
    color:gray;'>
    Personalized Learning Assistant
    </h4>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# SIDEBAR MENU
# -----------------------------------
selected = option_menu(

    menu_title=None,

    options=[
        "Home",
        "Roadmap",
        "Videos",
        "Mentor Chat",
        "Progress",
        "Settings"
    ],

    icons=[
        "house",
        "map",
        "camera-video",
        "chat",
        "graph-up",
        "gear"
    ],

    orientation="horizontal"
)

# -----------------------------------
# HOME TAB
# -----------------------------------
if selected == "Home":

    st.subheader(
        "Start Your Skill Journey"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(
            "https://images.unsplash.com/photo-1517836357463-d25dfeac3438",
            use_container_width=True
        )
        st.caption("Fitness")

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1522202176988-66273c2fd55f",
            use_container_width=True
        )
        st.caption("Languages")

    with col3:
        st.image(
            "https://images.unsplash.com/photo-1515879218367-8466d910aaa4",
            use_container_width=True
        )
        st.caption("Programming")

    st.divider()

    skill = st.text_input(
        "Skill"
    )

    goal = st.text_input(
        "Goal"
    )

    level = st.selectbox(
        "Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    months = st.number_input(
        "Months",
        min_value=1,
        max_value=24,
        value=3
    )

    hours = st.number_input(
        "Hours per day",
        min_value=1,
        max_value=10,
        value=2
    )

    if st.button(
        "Generate My Roadmap"
    ):

        with st.spinner(
            "Generating roadmap..."
        ):

            roadmap = (
                generate_roadmap(
                    skill,
                    goal,
                    level,
                    months,
                    hours
                )
            )

            st.session_state[
                "roadmap"
            ] = roadmap

            st.session_state[
                "skill"
            ] = skill

            st.success(
                "Roadmap Generated!"
            )

            st.write(
                roadmap
            )

# -----------------------------------
# ROADMAP TAB
# -----------------------------------
elif selected == "Roadmap":

    st.subheader(
        "Your Learning Roadmap"
    )

    roadmap = (
        st.session_state
        .get(
            "roadmap",
            "Generate roadmap first."
        )
    )

    st.write(
        roadmap
    )

# -----------------------------------
# VIDEOS TAB
# -----------------------------------
elif selected == "Videos":

    st.subheader(
        "Recommended Videos"
    )

    skill = (
        st.session_state
        .get("skill")
    )

    if skill:

        videos = (
            recommend_videos(
                skill
            )
        )

        for v in videos:

            st.markdown(
                f"""
                - [{v['title']}]
                ({v['url']})
                """
            )

    st.divider()

    st.subheader(
        "Video Summary"
    )

    video_url = st.text_input(
        "Paste YouTube URL"
    )

    if st.button(
        "Summarize Video"
    ):

        summary = (
            summarize_video(
                video_url
            )
        )

        st.write(
            summary
        )

# -----------------------------------
# CHAT TAB
# -----------------------------------
elif selected == "Mentor Chat":

    st.subheader(
        "Continue Learning"
    )

    username = st.text_input(
        "Username"
    )

    message = st.text_input(
        "Ask mentor"
    )

    if st.button(
        "Send"
    ):

        save_chat(
            username,
            message
        )

        st.success(
            "Saved!"
        )

    history = (
        load_chat(
            username
        )
    )

    for msg in history:

        st.chat_message(
            "user"
        ).write(msg)

# -----------------------------------
# PROGRESS TAB
# -----------------------------------
elif selected == "Progress":

    st.subheader(
        "Track Progress"
    )

    completed = st.text_area(
        "What did you complete?"
    )

    if st.button(
        "Update Progress"
    ):

        st.success(
            "Progress Updated!"
        )

# -----------------------------------
# SETTINGS TAB
# -----------------------------------
elif selected == "Settings":

    st.subheader(
        "Calendar & Email"
    )

    skill = (
        st.session_state
        .get("skill")
    )

    time = st.text_input(
        "Preferred Time",
        "18:00"
    )

    if st.button(
        "Add Calendar"
    ):

        add_learning_schedule(
            skill,
            time
        )

        st.success(
            "Calendar Added!"
        )

    email = st.text_input(
        "Weekly Report Email"
    )

    if st.button(
        "Enable Weekly Report"
    ):

        roadmap = (
            st.session_state
            .get(
                "roadmap",
                ""
            )
        )

        send_weekly_email(
            email,
            skill,
            roadmap
        )

        st.success(
            "Email Sent!"
        )