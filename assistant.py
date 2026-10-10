from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import os

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Amit's Co-Pilot",
    layout="wide"
)

load_dotenv()

# ----------------------------
# OpenAI Client
# ----------------------------
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

role = st.selectbox(
    "Choose Domain",
    [
        "Banking Advisor",
        "Insurance Advisor",
        "Market Research Expert",
        "Legal Assistant"
    ]
)

prompts = {
   "Banking Advisor":"You are a senior retail banking advisor.Answer only banking-related questions.If the question is outside banking,politely say that the assistant onlyhandles banking topics.",
   "Insurance Advisor":"You are an insurance advisor.Explain policies, claims,premium calculations,and insurance conceptsusing simple language.",
   "Market Research Expert":"You are a senior market research consultant with 15 years of experience. Provide insights, customer analysis,survey interpretation,and business recommendations.",
   "Legal Assistant":"You are a senior lawyer"
}

SYSTEM_PROMPT = {
    
        "role": "system",
        "content": prompts.get(
            role,
            "You are a helpful AI assistant."
        )
}


# ----------------------------
# Session State
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:

    st.title("🤖 Amit's Co-Pilot")

    if st.button("➕ New Chat"):

        # Save current chat before switching
        if st.session_state.messages:
            st.session_state.chat_history[
                st.session_state.current_chat
            ] = st.session_state.messages.copy()

        chat_no = len(st.session_state.chat_history) + 1

        st.session_state.current_chat = f"Chat {chat_no}"
        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.subheader("Previous Chats")

    for chat_name in st.session_state.chat_history.keys():

        if st.button(chat_name, key=chat_name):

            st.session_state.current_chat = chat_name
            st.session_state.messages = st.session_state.chat_history[chat_name]

            st.rerun()

# ----------------------------
# Main Page
# ----------------------------
st.title("🤖 Amit's Co-Pilot")
st.caption(f"Current Conversation: {st.session_state.current_chat}")

# ----------------------------
# Display Previous Messages
# ----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ----------------------------
# Chat Input
# ----------------------------
user_input = st.chat_input("Ask something...")

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[SYSTEM_PROMPT] + st.session_state.messages
    )

    ai_reply = response.choices[0].message.content

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    # Save current chat
    st.session_state.chat_history[
        st.session_state.current_chat
    ] = st.session_state.messages.copy()

    st.rerun()