import streamlit as st
import pandas as pd

st.title("📥 Upload Your Dataset")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())
