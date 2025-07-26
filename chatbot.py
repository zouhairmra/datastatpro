import streamlit as st
from transformers import pipeline

# Load a financial Q&A model from Hugging Face
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="FinGPT/fingpt-mt_llama3-8b_lora")

generator = load_model()

def get_bot_response(prompt):
    try:
        result = generator(prompt, max_length=200, do_sample=True, temperature=0.7)
        return result[0]["generated_text"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

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
