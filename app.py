import os
import streamlit as st
from google import genai

st.set_page_config(
    page_title="MemoryBot AI",
    page_icon="🤖",
    layout="wide"
)

# ---------- Header ----------
st.title("🤖 MemoryBot AI")
st.caption("Your personal AI assistant with conversation memory")

api_key = None

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Load it from Colab Secrets.")
    st.stop()

# ---------- Create Gemini client and chat ----------
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.8-flash"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Sidebar ----------
with st.sidebar:
    st.header("🧠 MemoryBot")
    st.write("Your AI conversation assistant")
    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat = st.session_state.client.chats.create(
            model="gemini-3.8-flash"
        )
        st.rerun()

    st.subheader("💬 Chat History")

    user_messages = [
        message["content"]
        for message in st.session_state.messages
        if message["role"] == "user"
    ]

    if user_messages:
        for index, message in enumerate(user_messages, start=1):
            st.caption(f"{index}. {message[:60]}")
    else:
        st.caption("Your messages will appear here.")

    st.divider()
    st.caption("Powered by Google Gemini")

# ---------- Display conversation ----------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------- Chat input ----------
user_input = st.chat_input("Ask MemoryBot anything...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("MemoryBot is thinking..."):
            try:
                response = st.session_state.chat.send_message(user_input)
                answer = response.text or "I couldn't generate a response."

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Gemini error: {e}")
