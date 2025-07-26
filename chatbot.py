import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import openai
from openai import OpenAI
import sys
import os
st.title("🧠 AI Economics Assistant (Mistral-7B)")

api_key = st.text_input("🔑 Enter your Together AI API Key", type="password")
prompt = st.text_area("💬 Ask a question:", height=150)

if st.button("Generate Answer"):
    if not api_key:
        st.error("❌ Please enter your API key.")
    elif not prompt.strip():
        st.error("❌ Please write a prompt.")
    else:
        url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mistralai/Mistral-7B-Instruct-v0.2",  # ✅ Update this with your chosen model
            "messages": [
                {"role": "system", "content": "You are an expert in economics."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }

        try:
            resp = requests.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                answer = resp.json()["choices"][0]["message"]["content"]
                st.markdown("### 🤖 Answer")
                st.write(answer)
            else:
                st.error(f"❌ HTTP {resp.status_code}: {resp.json()}")
        except Exception as e:
            st.error(f"❌ Error: {e}")
# Optional: Let the user pick a model from supported options
        with st.expander("🧠 Model Options"):
            available_models = [
                "mistralai/Mistral-7B-Instruct-v0.2",
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "meta-llama/Llama-2-7b-chat-hf"
            ]
            selected_model = st.selectbox("Choose a model", available_models, index=0)
            payload["model"] = selected_model
# Additional Features Below (do not change original block)

        # Allow user to adjust temperature and max_tokens dynamically
        with st.expander("🔧 Advanced Settings"):
            user_temp = st.slider("Temperature (creativity)", 0.0, 1.0, 0.7, 0.05)
            user_max_tokens = st.slider("Max tokens (response length)", 256, 4096, 1024, 128)

        payload["temperature"] = user_temp
        payload["max_tokens"] = user_max_tokens
