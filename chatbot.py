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
    st.markdown("Ask anything about **economics** or **finance** in **English or Arabic**. The bot remembers previous answers.")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Button to clear only user messages
    if st.button("🧹 Clear User Messages"):
        st.session_state.chat_history = [msg for msg in st.session_state.chat_history if msg["role"] == "assistant"]
        st.rerun()

    # Display chat history
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"🧑 **You:** {chat['content']}")
        else:
            st.markdown(f"🤖 **Bot:** {chat['content']}")

    # Input box
    user_input = st.text_input("💬 Enter your message", key="user_input")

    if st.button("Ask") and user_input.strip():
        user_msg = user_input.strip()
        st.session_state.chat_history.append({"role": "user", "content": user_msg})

        # Build prompt with full assistant history + current user input
        conversation_prompt = "You are a helpful assistant specialized in economics and finance. Respond clearly in the same language as the user.\n"
        for chat in st.session_state.chat_history:
            role = "User" if chat["role"] == "user" else "Assistant"
            conversation_prompt += f"{role}: {chat['content']}\n"
        conversation_prompt += "Assistant:"

        with st.spinner("Thinking..."):
            payload = {
                "model": "mistralai/Mistral-7B-Instruct-v0.2",
                "prompt": conversation_prompt,
                "max_tokens": 256,
                "temperature": 0.7,
            }

            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload)
                response.raise_for_status()
                result = response.json()
                answer = result["choices"][0]["text"].strip()
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.rerun()

            except requests.exceptions.HTTPError as err:
                st.error(f"❌ Error {err.response.status_code}: {err.response.text}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")
