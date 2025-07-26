import streamlit as st
import requests

# Read the API key from the 'together' section
TOGETHER_API_KEY = st.secrets["together"]["api_key"]

headers = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

url = "https://api.together.xyz/v1/completions"

payload = {
    "model": "mistralai/Mistral-7B-Instruct-v0.2",
    "prompt": "Explain inflation in simple terms.",
    "max_tokens": 128,
    "temperature": 0.7
}

response = requests.post(url, headers=headers, json=payload)

st.write("Response:", response.json())
