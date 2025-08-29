import streamlit as st
import time
import base64
import tempfile
from gtts import gTTS

from modules.resume_parser import parse_resume
from modules.question_generator import generate_questions
from modules.faq_bot import faq_chatbot
from modules.video_recorder import video_interview_ui

st.set_page_config(layout="wide", page_title="Interview Bot")

# -------------------- Initialize Session --------------------
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "timer" not in st.session_state:
    st.session_state.timer = 60
if "video_started" not in st.session_state:
    st.session_state.video_started = False
if "last_spoken_index" not in st.session_state:
    st.session_state.last_spoken_index = -1
if "waiting_for_audio" not in st.session_state:
    st.session_state.waiting_for_audio = False
if "page" not in st.session_state:
    st.session_state.page = "Upload Resume"

st.title("🤖 Interview Bot")

# -------------------- Custom Sidebar Menu --------------------
sidebar_style = """
    <style>
        .stButton > button {
            width: 100%;
            background-color: #262730;
            color: white;
            padding: 10px;
            border-radius: 10px;
            text-align: left;
            font-size: 16px;
            transition: all 0.3s ease-in-out;
            border: none;
            margin-bottom: 10px;
        }
        .stButton > button:hover {
            background-color: #4CAF50;
            transform: scale(1.05);
            box-shadow: 0px 0px 10px rgba(76, 175, 80, 0.8);
        }
        .active-btn {
            background-color: #4CAF50 !important;
            font-weight: bold;
        }
    </style>
"""
st.markdown(sidebar_style, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Explore")

    if st.button("📄 Upload Resume", key="resume_btn"):
        st.session_state.page = "Upload Resume"
    if st.button("🎥 Interview", key="interview_btn"):
        st.session_state.page = "Interview"
    if st.button("💬 FAQ Bot", key="faq_btn"):
        st.session_state.page = "FAQ Bot"

# Highlight active page
active_page = st.session_state.page
js_highlight = f"""
    <script>
    var buttons = window.parent.document.querySelectorAll('.stButton > button');
    buttons.forEach(btn => {{
        if(btn.innerText.includes("{active_page.split()[0]}")) {{
            btn.classList.add("active-btn");
        }}
    }});
    </script>
"""
st.markdown(js_highlight, unsafe_allow_html=True)

# -------------------- Helper: Speak Question --------------------
def speak_text(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        audio_file = tmp.name

    with open(audio_file, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    return audio_html

# -------------------- Resume Upload --------------------
if st.session_state.page == "Upload Resume":
    st.header("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    if uploaded_file:
        resume_text = parse_resume(uploaded_file)
        st.session_state.resume_text = resume_text
        st.success("Resume uploaded & parsed successfully!")
        st.text_area("Extracted Resume Text", resume_text, height=300)

        if st.button("Start Interview"):
            st.session_state.questions = generate_questions(resume_text)
            st.session_state.current_index = 0
            st.session_state.timer = 60
            st.session_state.video_started = False
            st.session_state.last_spoken_index = -1
            st.session_state.waiting_for_audio = True   # ✅ ensure Q1 is spoken immediately
            st.success("Interview setup completed! Go to 'Interview' section in sidebar.")

# -------------------- Interview --------------------
elif st.session_state.page == "Interview":
    st.header("🎥 AI Interview")

    if not st.session_state.questions:
        st.warning("⚠️ Please upload a resume and start interview first.")
    else:
        col1, col2 = st.columns([1.2, 1])
        recording_active = video_interview_ui(col2)

        if recording_active:
            with col1:
                st.subheader(f"Question {st.session_state.current_index + 1}")
                current_q = st.session_state.questions[st.session_state.current_index]
                st.write(current_q)

                # --- Speak question when waiting_for_audio is True ---
                if st.session_state.waiting_for_audio:
                    audio_html = speak_text(current_q)
                    st.markdown(audio_html, unsafe_allow_html=True)
                    st.info("🔊 AI is reading the question… Please listen.")
                    st.session_state.waiting_for_audio = False
                    st.session_state.last_spoken_index = st.session_state.current_index
                    st.stop()

                # --- Timer logic (after question audio finishes) ---
                timer_placeholder = st.empty()
                if st.session_state.timer > 0:
                    timer_placeholder.markdown(f"⏰ Time left: **{st.session_state.timer}** seconds")
                    st.session_state.timer -= 1
                    time.sleep(1)
                    st.rerun()
                else:
                    timer_placeholder.markdown("⏰ Time's up!")

                # Navigation buttons
                if st.button("➡️ Next"):
                    if st.session_state.current_index < len(st.session_state.questions) - 1:
                        st.session_state.current_index += 1
                        st.session_state.timer = 60
                        st.session_state.waiting_for_audio = True   # ✅ each new Q will be spoken
                        st.experimental_rerun()
                    else:
                        st.success("✅ You have completed all questions!")

                if st.button("🏁 Finish Test"):
                    st.success("🎉 Interview finished! Thanks for your time.")
                    st.session_state.questions = []
                    st.session_state.current_index = 0
                    st.session_state.timer = 60
                    st.session_state.resume_text = ""
                    st.session_state.video_started = False
                    st.session_state.last_spoken_index = -1
                    st.session_state.waiting_for_audio = False

# -------------------- FAQ Bot --------------------
elif st.session_state.page == "FAQ Bot":
    st.header("💬 HR FAQ Chatbot")
    faq_chatbot()
