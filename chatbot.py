import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

def query_huggingface(prompt):
    try:
        response = requests.post(API_URL, json={"inputs": prompt})
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        else:
            return "🤖 Sorry, I couldn't generate a response."
    except requests.exceptions.RequestException as e:
        return f"⚠️ Request error: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

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

        response = query_huggingface(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
