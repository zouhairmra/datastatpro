import streamlit as st
import requests

# ✅ Directly define your API key and endpoint here
HF_API_KEY = "hf_YourTokenHere"
HF_API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"

def query(payload):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return f"❌ Error {response.status_code}: {response.text}"

def run_chatbot():
    st.title("💬 Economics & Finance Chatbot")

    history = st.session_state.get("history", [])
    user_input = st.text_input("Ask a question about economics or finance:")

    if user_input:
        with st.spinner("Thinking..."):
            prompt = f"<|user|>\n{user_input}\n<|assistant|>"
            output = query({"inputs": prompt})
            history.append((user_input, output))
            st.session_state["history"] = history

    for user_q, bot_a in reversed(history):
        st.markdown(f"**You**: {user_q}")
        st.markdown(f"**Bot**: {bot_a}")
