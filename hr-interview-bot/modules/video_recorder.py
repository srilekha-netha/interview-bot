import streamlit as st
from streamlit_webrtc import webrtc_streamer

def video_interview_ui(container):
    container.subheader("Candidate Recording")

    # If recording not started yet → show button
    if not st.session_state.get("video_started", False):
        if container.button("▶️ Start Recording"):
            st.session_state.video_started = True
            st.rerun()
        return None

    # Once started → show video recorder in RIGHT column
    with container:
        webrtc_streamer(
            key="interview_whole",
            media_stream_constraints={"video": True, "audio": True},
            async_processing=True
        )
        container.info("📹 Recording in progress… Answer confidently!")

    return True
