import streamlit as st
import requests

API_URL = st.secrets["HF_API_URL"]
API_KEY = st.secrets["HF_API_KEY"]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def ask_mistral(question):
    prompt = f"[INST] {question} [/INST]"
    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True  # Important for free-tier use
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    output = response.json()

    if isinstance(output, list):
        return output[0]["generated_text"]
    else:
        return str(output)

def run_chatbot():
    st.title("🤖 Economics & Finance Chatbot")
    st.markdown("Ask a question on **economics or finance**.")

    if "history" not in st.session_state:
        st.session_state.history = []

    user_input = st.text_input("💬 Your question:", key="user_input")

    if st.button("Ask") and user_input:
        st.session_state.history.append(("You", user_input))

        with st.spinner("Thinking..."):
            try:
                answer = ask_mistral(user_input)
            except Exception as e:
                answer = f"❌ Error: {e}"

        st.session_state.history.append(("Bot", answer))

    for speaker, msg in st.session_state.history:
        st.markdown(f"**{speaker}:** {msg}")

