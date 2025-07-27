import streamlit as st
import requests
from langdetect import detect
from googletrans import Translator

def run_chatbot():
    st.set_page_config(page_title="💬 Chatbot", layout="centered")

    API_KEY = st.secrets["together"]["api_key"]
    API_URL = "https://api.together.xyz/v1/completions"
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    translator = Translator()

    st.title("🤖 Bilingual Chatbot")
    st.markdown("Ask anything in **English or Arabic** – the assistant will detect your language and respond accordingly.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("💬 Your question:")

    if st.button("Ask") and user_input.strip():
        user_msg = user_input.strip()

        # Detect language
        try:
            lang = detect(user_msg)
        except:
            lang = "en"  # fallback

        st.session_state.chat_history.append({"role": "user", "content": user_msg})

        # Build full prompt
        full_prompt = "You are a helpful assistant that replies in the same language as the user.\n"
        for msg in st.session_state.chat_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            full_prompt += f"{role}: {msg['content']}\n"
        full_prompt += "Assistant:"

        with st.spinner("Thinking..."):
            payload = {
                "model": "mistralai/Mistral-7B-Instruct-v0.2",
                "prompt": full_prompt,
                "max_tokens": 512,
                "temperature": 0.7,
            }

            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload)
                response.raise_for_status()
                raw_output = response.json()["choices"][0]["text"].strip()
                answer = raw_output.split("User:")[0].split("Assistant:")[0].strip()

                # Translate if needed
                if lang == "ar":
                    answer = translator.translate(answer, dest="ar").text

                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.markdown(f"🤖 **Bot:** {answer}")
            except requests.exceptions.HTTPError as err:
                st.error(f"❌ API Error: {err.response.status_code} - {err.response.text}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")

    if st.button("🧹 Clear User Messages"):
        st.session_state.chat_history = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
        st.rerun()
