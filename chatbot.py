import streamlit as st
import requests

def run_chatbot():
    st.set_page_config(page_title="📊 Economics & Finance Chatbot", layout="centered")

    # Load Together API key from Streamlit secrets
    API_KEY = st.secrets["together"]["api_key"]

    # Together Inference API endpoint
    API_URL = "https://api.together.xyz/v1/completions"
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    st.title("💡 Economics & Finance Chatbot")
    st.markdown("Ask anything about **economics** or **finance**, and get helpful answers powered by Mistral-7B.")

    user_input = st.text_input("💬 Enter your question:", "")

    if st.button("Ask") and user_input.strip():
        with st.spinner("Thinking..."):
            payload = {
                "model": "mistralai/Mistral-7B-Instruct-v0.2",
                "prompt": f"Answer the following question in a clear and concise way:\n{user_input}\n",
                "max_tokens": 256,
                "temperature": 0.7,
            }

            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload)
                response.raise_for_status()
                result = response.json()
                answer = result["choices"][0]["text"]
                st.success("✅ Answer:")
                st.write(answer.strip())

            except requests.exceptions.HTTPError as err:
                st.error(f"❌ Error {err.response.status_code}: {err.response.text}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
