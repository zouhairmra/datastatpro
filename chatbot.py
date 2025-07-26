# chatbot.py

from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_model():
    return pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2")

generator = load_model()

def run_chatbot():
    st.title("💬 Economics & Finance Chatbot")

    user_input = st.text_input("Ask me anything about economics or finance:")

    if user_input:
        with st.spinner("Thinking..."):
            result = generator(user_input, max_length=100, temperature=0.7)[0]["generated_text"]
            st.success(result)
