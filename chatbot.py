import streamlit as st
import requests
import os

# Hugging Face Inference API settings
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
HF_TOKEN = os.getenv("HF_API_TOKEN")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def get_bot_response(prompt):
    return query({"inputs": prompt})

def run_chatbot():
    st.set_page_config(page_title="EconBot 💼", layout="centered")
    st.title("💬 EconBot - Economics & Finance Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about inflation, GDP, interest rates..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
