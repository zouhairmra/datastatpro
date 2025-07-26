import streamlit as st
import requests

# Secure API key access
TOGETHER_API_KEY = st.secrets["together"]["api_key"]

def get_chat_response(prompt):
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.95,
        "repetition_penalty": 1.1,
        "stop": ["User:", "Assistant:"]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        return f"❌ Error {response.status_code}: {response.text}"

def run_chatbot():
    st.title("🧠 ChatBot - Mistral 7B Assistant")
    st.caption("Powered by Together AI & Mistral-7B-Instruct-v0.2")

    # Initialize session state
    if "history" not in st.session_state:
        st.session_state.history = []

    # Display chat history
    for message in st.session_state.history:
        if message["role"] == "user":
            st.markdown(f"**🧑 You:** {message['content']}")
        else:
            st.markdown(f"**🤖 Bot:** {message['content']}")

    # Input field
    user_input = st.text_input("💬 Ask your question", key="user_input")

    if st.button("Send") and user_input.strip():
        # Append user message
        st.session_state.history.append({"role": "user", "content": user_input.strip()})

        # Construct full prompt
        full_prompt = "You are a helpful assistant.\n\n"
        for msg in st.session_state.history:
            role = "User" if msg["role"] == "user" else "Assistant"
            full_prompt += f"{role}: {msg['content']}\n"
        full_prompt += "Assistant:"

        with st.spinner("🤖 Thinking..."):
            response = get_chat_response(full_prompt)

        # Append bot response
        st.session_state.history.append({"role": "assistant", "content": response})
        # Clear input
        st.session_state["user_input"] = ""

    # Option to clear chat
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []
        st.experimental_rerun()
