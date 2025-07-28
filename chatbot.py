import streamlit as st
import requests

def run_chatbot():
    st.set_page_config(page_title="📊 Economics & Finance Chatbot", layout="centered")

    API_KEY = st.secrets["together"]["api_key"]
    API_URL = "https://api.together.xyz/v1/completions"
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    st.title("💡 Economics & Finance Chatbot")
    st.markdown("Ask anything about **economics** or **finance**, in **English or Arabic**. The assistant remembers the conversation.")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display past messages
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"🧑 **You:** {msg['content']}")
        else:
            st.markdown(f"🤖 **Bot:** {msg['content']}")

    # Clear only user messages
    if st.button("🧹 Clear User Messages"):
        st.session_state.chat_history = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
        st.rerun()

    # User input
    user_input = st.text_input("💬 Enter your message")

    if st.button("Ask") and user_input.strip():
        user_msg = user_input.strip()
        st.session_state.chat_history.append({"role": "user", "content": user_msg})

        # Build conversation prompt
        full_prompt = "You are a helpful assistant that answers clearly and intelligently in the same language used by the user.\n"
        for msg in st.session_state.chat_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            full_prompt += f"{role}: {msg['content']}\n"
        full_prompt += "Assistant:"

        # API call
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
                answer = response.json()["choices"][0]["text"].strip()
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.rerun()
            except requests.exceptions.HTTPError as err:
                st.error(f"❌ Error {err.response.status_code}: {err.response.text}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
# --- ADDED SECTION: Custom system prompt ---
        system_prompt = "You are a helpful assistant that answers clearly and intelligently in the same language used by the user.\n"
# --- ADDED SECTION: Model selector ---
with st.sidebar:
    st.markdown("### ⚙️ Model & UI Settings")

    model_choice = st.selectbox(
        "Choose a model",
        [
            "mistralai/Mistral-7B-Instruct-v0.2",
            "meta-llama/Llama-2-7b-chat-hf",
            "NousResearch/Nous-Hermes-2-Mistral-7B-DPO"
        ],
        index=0
    )


