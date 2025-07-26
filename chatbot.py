import streamlit as st
import requests
import streamlit as st
import os
import requests

st.write("Secrets content:", st.secrets)  # DEBUG LINE

TOGETHER_API_KEY = st.secrets["together"]["api_key"]

def get_chat_response(prompt):
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.95,
        "repetition_penalty": 1.1,
        "stop": ["User:", "Assistant:"]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        return f"❌ Error {response.status_code}: {response.text}"

def run_chatbot():
    st.title("🧠 ChatBot - Mistral 7B Assistant")
    st.caption("Powered by Together AI & Mistral-7B-Instruct-v0.2")

    if "history" not in st.session_state:
        st.session_state.history = []

    # Show chat history
    for message in st.session_state.history:
        if message["role"] == "user":
            st.markdown(f"**🧑 You:** {message['content']}")
        else:
            st.markdown(f"**🤖 Bot:** {message['content']}")

    # Input area with key user_input
user_input = st.text_input("💬 Ask a question", key="user_input")

if st.button("Send") and user_input.strip():
    st.session_state.history.append({"role": "user", "content": user_input.strip()})

    # Build prompt from conversation history
    full_prompt = "You are a helpful assistant.\n\n"
    for msg in st.session_state.history:
        role = "User" if msg["role"] == "user" else "Assistant"
        full_prompt += f"{role}: {msg['content']}\n"
    full_prompt += "Assistant:"

    with st.spinner("🤖 Bot is thinking..."):
        response = get_chat_response(full_prompt)

    st.session_state.history.append({"role": "assistant", "content": response})

    # Clear the text input by setting session_state key to empty string
    st.session_state["user_input"] = ""
