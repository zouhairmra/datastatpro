import streamlit as st

st.set_page_config(page_title="EconBot 💼", layout="centered")

st.title("💬 EconBot - Economics & Finance Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask about inflation, GDP, interest rates..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Simulated bot response
    def get_bot_response(text):
        text = text.lower()
        if "inflation" in text:
            return "Inflation is the rate at which prices increase over time."
        elif "gdp" in text:
            return "GDP stands for Gross Domestic Product, a measure of a country's economic output."
        elif "interest rate" in text:
            return "Interest rates are set by central banks to control inflation and economic growth."
        else:
            return "I'm still learning! Try asking about inflation, GDP, or interest rates."

    response = get_bot_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
