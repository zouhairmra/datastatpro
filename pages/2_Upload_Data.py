import streamlit as st
import pandas as pd

st.title("📤 Upload Your Data")

uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded data:")
    st.dataframe(df.head())
