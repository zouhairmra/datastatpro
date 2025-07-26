# chatbot.py

import streamlit as st
import requests
import os

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

    # Show the conversation so far
    for message in st.session_state.history:
        if message["role"] == "user":
            st.markdown(f"**🧑 You:** {message['content']}")
        else:
            st.markdown(f"**🤖 Bot:** {message['content']}")

    user_input = st.text_input("💬 Ask a question", key="user_input")
    if user_input:
        # Append user input to history
        st.session_state.history.append({"role": "user", "content": user_input})

        # Create full prompt from history
        full_prompt = "You are a helpful assistant.\n\n"
        for msg in st.session_state.history:
            if msg["role"] == "user":
                full_prompt += f"User: {msg['content']}\n"
            else:
                full_prompt += f"Assistant: {msg['content']}\n"
        full_prompt += "Assistant:"

        # Get model response
        response = get_chat_response(full_prompt)

        # Append assistant response to history
        st.session_state.history.append({"role": "assistant", "content": response})

        # Clear input field
        st.rerun()
