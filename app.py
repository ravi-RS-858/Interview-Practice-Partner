import streamlit as st
from agent import InterviewAgent
from voice_mode import VoiceInterface

st.set_page_config(page_title="AI Interview Partner", layout="centered")

if "agent" not in st.session_state:
    st.session_state.agent = InterviewAgent()

if "history" not in st.session_state:
    st.session_state.history = []

st.title("AI Interview Practice Partner")

role = st.text_input("Enter role you're preparing for (e.g., SDE, Sales, Data Analyst):")

use_voice = st.checkbox("Enable Voice Mode")

if st.button("Start Interview"):
    if role.strip():
        first_q = st.session_state.agent.start_interview(role)
        st.session_state.history = [("bot", first_q)]
        if use_voice:
            vi = VoiceInterface()
            vi.speak(first_q)
        st.rerun()

for speaker, text in st.session_state.history:
    if speaker == "bot":
        st.markdown(f"~Interviewer: {text}")
    else:
        st.markdown(f"-You: {text}")

user_text = st.text_input("Type your answer here:")

if st.button("Submit Typed Answer") and user_text.strip():
    st.session_state.history.append(("user", user_text))
    reply = st.session_state.agent.process_answer(user_text)
    st.session_state.history.append(("bot", reply))
    if use_voice:
        vi = VoiceInterface()
        vi.speak(reply)
    st.rerun()

if use_voice and st.button("Speak Your Answer"):
    vi = VoiceInterface()

    with st.spinner("Listening... You have up to 80 seconds. Start speaking now."):
        spoken = vi.listen(max_seconds=80)

    if spoken:
        st.success("Recording stopped. Processing your answer...")
        st.write(f"-You (voice): {spoken}")
        st.session_state.history.append(("user", spoken))
        reply = st.session_state.agent.process_answer(spoken)
        st.session_state.history.append(("bot", reply))
        vi.speak(reply)
        st.rerun()
    else:
        st.warning("Unable to understand your voice. Try again.")


if st.button("End Interview & Get Feedback"):
    feedback = st.session_state.agent.get_feedback()
    st.subheader("Final Feedback")
    st.write(feedback)
    if use_voice:
        vi = VoiceInterface()
        vi.speak("Here is your feedback. Please check the screen.")
