import streamlit as st
import json
import os

st.set_page_config(
    page_title="AI Skill Mentor",
    page_icon="🚀",
    layout="wide"
)

os.makedirs("storage", exist_ok=True)

USER_FILE = "storage/users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)


def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=4)


st.title("🚀 AI Skill Mentor")

username = st.sidebar.text_input(
    "Enter Username"
)

if not username:
    st.info(
        "Enter username first."
    )
    st.stop()

users = load_users()

user_data = users.get(
    username,
    {}
)

tab1, tab2 = st.tabs([
    "🏠 Home",
    "🗺 Roadmap"
])

with tab1:

    st.subheader(
        "Start Learning"
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

    if st.button(
        "Generate Roadmap"
    ):

        roadmap = f"""
Skill: {skill}

Goal: {goal}

Beginner roadmap generated.
"""

        users[username] = {
            "skill": skill,
            "goal": goal,
            "roadmap": roadmap
        }

        save_users(users)

        st.success(
            "Roadmap saved!"
        )

with tab2:

    roadmap = user_data.get(
        "roadmap"
    )

    if roadmap:
        st.write(roadmap)
    else:
        st.warning(
            "No roadmap yet."
        )