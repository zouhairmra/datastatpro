import streamlit as st
import requests

# Load from Streamlit secrets
API_URL = st.secrets["HF_API_URL"]
API_KEY = st.secrets["HF_API_KEY"]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def query_huggingface(prompt):
    data = {
        "inputs": f"[INST] {prompt} [/INST]",
        "options": {"wait_for_model": True}
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# Streamlit app
def run_chatbot():
    st.title("🧠 Mistral Chatbot")

    user_input = st.text_input("Ask a question:")
    if st.button("Send") and user_input:
        with st.spinner("Thinking..."):
            output = query_huggingface(user_input)
            st.markdown(f"**Bot:** {output}")
