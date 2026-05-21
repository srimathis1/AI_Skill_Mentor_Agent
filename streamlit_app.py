import streamlit as st
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

# ===================================
# PAGE CONFIG
# ===================================
st.set_page_config(
    page_title="AI Skill Mentor",
    page_icon="🚀",
    layout="wide"
)

# ===================================
# STORAGE SETUP
# ===================================
os.makedirs(
    "storage",
    exist_ok=True
)

USER_FILE = (
    "storage/users.json"
)

CHAT_FILE = (
    "storage/chat_history.json"
)

# create json files
for file in [
    USER_FILE,
    CHAT_FILE
]:

    if not os.path.exists(
        file
    ):
        with open(
            file,
            "w"
        ) as f:

            json.dump(
                {},
                f
            )


# ===================================
# USER STORAGE
# ===================================
def load_users():

    with open(
        USER_FILE,
        "r"
    ) as f:

        return json.load(f)


def save_users(
    data
):

    with open(
        USER_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


# ===================================
# HEADER
# ===================================
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

# ===================================
# LOGIN
# ===================================
username = st.sidebar.text_input(
    "Enter Username"
)

if not username:

    st.info(
        "Enter username to continue."
    )

    st.stop()

users = load_users()

user_data = users.get(
    username,
    {}
)

# ===================================
# TABS
# ===================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Home",
    "🗺 Roadmap",
    "🎥 Videos",
    "💬 Mentor Chat",
    "📈 Progress",
    "⚙ Settings"
])

# ===================================
# HOME
# ===================================
with tab1:

    st.subheader(
        "Start Learning"
    )

    st.image(
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3",
        use_container_width=True
    )

    skill = st.text_input(
        "Skill",
        value=user_data.get(
            "skill",
            ""
        )
    )

    goal = st.text_input(
        "Goal",
        value=user_data.get(
            "goal",
            ""
        )
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
        "Hours Per Day",
        min_value=1,
        max_value=12,
        value=2
    )

    if st.button(
        "Generate Roadmap"
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

            users[
                username
            ] = {

                "skill":
                skill,

                "goal":
                goal,

                "level":
                level,

                "months":
                months,

                "hours":
                hours,

                "roadmap":
                roadmap
            }

            save_users(
                users
            )

            st.success(
                "Roadmap saved!"
            )

            st.write(
                roadmap
            )

# ===================================
# ROADMAP
# ===================================
with tab2:

    st.subheader(
        "Saved Roadmap"
    )

    roadmap = user_data.get(
        "roadmap"
    )

    if roadmap:

        st.write(
            roadmap
        )

    else:

        st.warning(
            "Generate roadmap first."
        )

# ===================================
# VIDEOS
# ===================================
with tab3:

    st.subheader(
        "Recommended Videos"
    )

    skill_name = user_data.get(
        "skill"
    )

    if skill_name:

        videos = (
            recommend_videos(
                skill_name
            )
        )

        for v in videos:

            st.markdown(
                f"### [{v['title']}]({v['url']})"
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

# ===================================
# CHAT
# ===================================
with tab4:

    st.subheader(
        "Continue Learning"
    )

    msg = st.text_input(
        "Ask mentor"
    )

    if st.button(
        "Send Message"
    ):

        save_chat(
            username,
            msg
        )

        st.success(
            "Message saved!"
        )

    history = (
        load_chat(
            username
        )
    )

    if history:

        for h in history:

            st.chat_message(
                "user"
            ).write(h)

# ===================================
# PROGRESS
# ===================================
with tab5:

    st.subheader(
        "Track Progress"
    )

    progress = st.text_area(
        "What did you complete?"
    )

    if st.button(
        "Save Progress"
    ):

        st.success(
            "Progress saved!"
        )

# ===================================
# SETTINGS
# ===================================
with tab6:

    st.subheader(
        "Calendar & Email"
    )

    preferred_time = st.text_input(
        "Preferred Time",
        value="18:00"
    )

    if st.button(
        "Add Calendar Event"
    ):

        add_learning_schedule(
            user_data.get(
                "skill",
                ""
            ),
            preferred_time
        )

        st.success(
            "Calendar event added!"
        )

    st.divider()

    email = st.text_input(
        "Email"
    )

    if st.button(
        "Enable Weekly Report"
    ):

        send_weekly_email(
            email,
            user_data.get(
                "skill",
                ""
            ),
            user_data.get(
                "roadmap",
                ""
            )
        )

        st.success(
            "Weekly email sent!"
        )