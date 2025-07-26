from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

generator = load_model()

def ask_bot(question):
    response = generator(question, max_length=100, temperature=0.7)[0]["generated_text"]
    return response
