import streamlit as st
import requests

def run_chatbot():
    st.title("💬 Economics Chatbot (Mistral-7B via Hugging Face)")

    user_input = st.text_input("Ask something about economics or finance:")

    if user_input:
        with st.spinner("Thinking..."):
            answer = ask_huggingface(user_input)
            st.markdown(f"**Bot:** {answer}")

def ask_huggingface(prompt):
    api_url = st.secrets["HF_API_URL"]
    headers = {
        "Authorization": f"Bearer {st.secrets['HF_API_KEY']}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 100}
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        try:
            return result[0]["generated_text"]
        except Exception:
            return result
    else:
        return f"❌ Error {response.status_code}: {response.text}"
