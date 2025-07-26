import streamlit as st
from transformers import pipeline

# Set up the chatbot pipeline from Hugging Face (no API key needed)
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="mistralai/Mistral-7B-Instruct-v0.2",
        max_new_tokens=256,
        temperature=0.7
    )

# Load model once
generator = load_model()

# Streamlit UI
st.set_page_config(page_title="EcoChat 🤖📊", page_icon="💬")
st.title("💬 Economics & Finance Chatbot")
st.info("Ask any question about economics, finance, markets, or macro theory.")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("❓ Your Question:", placeholder="E.g., What causes inflation?")

if st.button("🧠 Get Answer"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        # Add user question to history
        st.session_state.history.append(("user", user_input))

        # Prompt for instruction-tuned model
        full_prompt = f"[INST] You are an economics and finance expert. Answer clearly:\n\n{user_input} [/INST]"

        with st.spinner("Thinking..."):
            output = generator(full_prompt)[0]["generated_text"]

        # Extract response after the instruction
        answer = output.split("[/INST]")[-1].strip()
        st.session_state.history.append(("bot", answer))

# Display chat history
for speaker, text in reversed(st.session_state.history):
    if speaker == "user":
        st.markdown(f"**🧑‍🎓 You:** {text}")
    else:
        st.markdown(f"**🤖 EcoBot:** {text}")
