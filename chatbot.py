import requests
import streamlit as st

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def ask_mistral(prompt):
    payload = {
        "inputs": f"[INST] {prompt} [/INST]",
        "options": {"wait_for_model": True}
    }
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# Streamlit UI
st.title("💬 Economics Chatbot (Mistral)")

question = st.text_input("Ask your economics or finance question:")
if st.button("Submit"):
    if question:
        answer = ask_mistral(question)
        st.markdown(f"**Bot:** {answer}")
    else:
        st.warning("Please enter a question.")
