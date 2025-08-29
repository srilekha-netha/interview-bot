import streamlit as st
from streamlit_webrtc import webrtc_streamer
import time
import random

# ---------------- Mock AI Question Generator ----------------
def generate_questions(resume_text):
    base_questions = [
        "Tell me about yourself.",
        "What are your strengths and weaknesses?",
        "Why should we hire you?",
        "Can you describe a situation where you had to explain a complex concept to a non-technical audience, and how did you approach it?",
        "What is your biggest achievement so far?",
    ]
    random.shuffle(base_questions)
    return base_questions

# ---------------- Text-to-Speech via HTML ----------------
def speak_text(text):
    return f"""
        <script>
            var utterance = new SpeechSynthesisUtterance("{text}");
            utterance.rate = 1;
            speechSynthesis.speak(utterance);
        </script>
    """

# ---------------- Video Interview UI ----------------
def video_interview_ui(questions):
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
        st.session_state.timer = 60
        st.session_state.start_time = None
        st.session_state.video_started = False
        st.session_state.last_spoken_index = -1
        st.session_state.waiting_for_audio = True
        st.session_state.showed_audio_message = False

    total_qs = len(questions)

    col1, col2 = st.columns([1, 1])

    # Left side -> Questions
    with col1:
        if st.session_state.current_index < total_qs:
            current_q = questions[st.session_state.current_index]
            st.subheader(f"Question {st.session_state.current_index + 1}")
            st.write(current_q)

            # --- Speak question when waiting_for_audio is True ---
            if st.session_state.waiting_for_audio:
                audio_html = speak_text(current_q)
                audio_placeholder = st.empty()
                info_placeholder = st.empty()

                audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
                info_placeholder.info("🔊 AI is reading the question… Please listen.")

                # After one rerun, clear the info message
                st.session_state.waiting_for_audio = False
                st.session_state.last_spoken_index = st.session_state.current_index
                st.session_state.showed_audio_message = True
                st.stop()

            # Clear "AI is reading..." once question was already spoken
            if st.session_state.get("showed_audio_message", False):
                st.session_state.showed_audio_message = False  # reset
                info_placeholder = st.empty()
                info_placeholder.empty()

            # Timer logic
            if st.session_state.start_time is None:
                st.session_state.start_time = time.time()

            elapsed = int(time.time() - st.session_state.start_time)
            remaining = max(0, st.session_state.timer - elapsed)
            st.markdown(f"⏰ Time left: **{remaining} seconds**")

            if remaining == 0:
                st.session_state.current_index += 1
                st.session_state.start_time = None
                st.session_state.waiting_for_audio = True
                st.session_state.showed_audio_message = False
                st.rerun()
        else:
            st.success("✅ Interview Completed! Thank you for your responses.")

    # Right side -> Video
    with col2:
        st.subheader("🎥 Candidate Recording")
        webrtc_streamer(
            key="interview_video",
            media_stream_constraints={"video": True, "audio": True},
            async_processing=True,
        )

# ---------------- Main App ----------------
def main():
    st.set_page_config(page_title="AI Interviewer", layout="wide")

    st.sidebar.title("📌 Navigation")
    page = st.sidebar.radio("Go to:", ["Upload Resume", "Interview"])

    if page == "Upload Resume":
        st.title("📄 Upload Resume")
        uploaded_file = st.file_uploader("Upload your resume (txt format)", type=["txt"])
        if uploaded_file:
            resume_text = uploaded_file.read().decode("utf-8")
            st.session_state.resume_text = resume_text
            st.success("Resume uploaded successfully!")

            if st.button("Start Interview"):
                st.session_state.questions = generate_questions(resume_text)
                st.session_state.current_index = 0
                st.session_state.timer = 60
                st.session_state.video_started = False
                st.session_state.last_spoken_index = -1
                st.session_state.waiting_for_audio = True
                st.session_state.showed_audio_message = False   # ✅ reset
                st.success("Interview setup completed! Go to 'Interview' section in sidebar.")

    elif page == "Interview":
        st.title("🤖 AI Interview Session")
        if "questions" not in st.session_state:
            st.warning("⚠️ Please upload your resume and start the interview first.")
        else:
            video_interview_ui(st.session_state.questions)


if __name__ == "__main__":
    main()
