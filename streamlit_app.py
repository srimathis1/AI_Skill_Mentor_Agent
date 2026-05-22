import streamlit as st

from services.mentor_agent import (
    generate_learning_plan
)

from services.youtube_service import (
    recommend_videos
)

from services.calendar_service import (
    add_learning_schedule
)

from services.memory_service import (
    save_user
)

from services.video_summary_service import (
    summarize_video
)

# ==================================
# PAGE CONFIG
# ==================================
st.set_page_config(
    page_title="AI Skill Mentor",
    page_icon="🚀",
    layout="wide"
)

# ==================================
# SESSION STATE
# ==================================
if "plan" not in st.session_state:
    st.session_state.plan = None

if "summary" not in st.session_state:
    st.session_state.summary = None

# ==================================
# CUSTOM CSS
# ==================================
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# TITLE
# ==================================
st.markdown(
    '<div class="main-title">'
    'AI Skill Mentor Agent'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Personalized AI Learning Mentor'
    '</div>',
    unsafe_allow_html=True
)

# ==================================
# USERNAME
# ==================================
username = st.text_input(
    "Username"
)

# ==================================
# PROMPT
# ==================================
prompt = st.text_area(
    "Tell me your learning goal",

    placeholder="""
Example:

I want to learn Spring Boot
for placements in 3 months.

I can study 2 hours daily
after 8 PM.
"""
)

# ==================================
# GENERATE BUTTON
# ==================================
if st.button(
    "Generate My Learning Plan"
):

    if not username:

        st.warning(
            "Please enter username."
        )

        st.stop()

    if not prompt:

        st.warning(
            "Please enter learning goal."
        )

        st.stop()

    with st.spinner(
        "AI is building your roadmap..."
    ):

        try:

            plan = (
                generate_learning_plan(
                    prompt
                )
            )

            st.session_state.plan = (
                plan
            )

            save_user(
                username,
                plan.model_dump()
            )

            try:

                add_learning_schedule(
                    plan.skill,
                    plan.preferred_time
                )

            except Exception:
                pass

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

# ==================================
# SHOW PLAN
# ==================================
if st.session_state.plan:

    plan = (
        st.session_state.plan
    )

    st.success(
        "Learning Plan Generated!"
    )

    # ======================
    # DETAILS
    # ======================
    st.subheader(
        "Extracted Details"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"Skill: "
            f"{plan.skill}"
        )

        st.info(
            f"Goal: "
            f"{plan.goal}"
        )

    with col2:

        st.info(
            f"Duration: "
            f"{plan.duration_months}"
            f" months"
        )

        st.info(
            f"Study Time: "
            f"{plan.preferred_time}"
        )

    st.divider()

    # ======================
    # ROADMAP
    # ======================
    st.subheader(
        "Personalized Roadmap"
    )

    st.markdown(
        plan.roadmap
    )

    st.divider()

    # ======================
    # VIDEOS
    # ======================
    st.subheader(
        "Recommended Videos"
    )

    videos = (
        recommend_videos(
            plan.skill
        )
    )

    for video in videos:

        st.markdown(
            f"""
### [{video['title']}]
({video['url']})
"""
        )

    st.divider()

    # ======================
    # VIDEO SUMMARY
    # ======================
    st.subheader(
        "AI Video Summarization"
    )

    youtube_url = st.text_input(
        "Paste YouTube URL"
    )

    if st.button(
        "Summarize Video"
    ):

        if youtube_url:

            with st.spinner(
                "Generating summary..."
            ):

                try:

                    summary = (
                        summarize_video(
                            youtube_url
                        )
                    )

                    st.session_state.summary = (
                        summary
                    )

                except Exception as e:

                    st.error(
                        f"Summary Error: {e}"
                    )

    # SHOW SUMMARY
    if st.session_state.summary:

        st.success(
            "Summary Generated!"
        )

        st.markdown(
            st.session_state.summary
        )

    st.divider()

    # ======================
    # CALENDAR
    # ======================
    st.subheader(
        "Study Schedule"
    )

    st.success(
        f"""
Calendar scheduled
at {plan.preferred_time}
"""
    )