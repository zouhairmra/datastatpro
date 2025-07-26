# chatbot.py

import streamlit as st
import requests

API_URL = st.secrets["HF_API_URL"]
API_KEY = st.secrets["HF_API_KEY"]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def query_mistral(prompt):
    payload = {
        "inputs": f"[INST] {prompt} [/INST]",
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 512
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # will throw error if API fails
    return response.json()[0]["generated_text"]

def run_chatbot():
    st.title("📊 Mistral Chatbot for Economics and Finance")

    user_input = st.text_area("Ask a question about economics or finance:")
    if st.button("Ask"):
        with st.spinner("Thinking..."):
            try:
                answer = query_mistral(user_input)
                st.markdown(f"**Answer:**\n\n{answer}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
