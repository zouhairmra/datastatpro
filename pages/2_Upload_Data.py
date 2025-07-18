import streamlit as st
import pandas as pd

st.title("📤 Upload Your Dataset")

uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1]
    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")
    st.dataframe(df)
    st.markdown("### Data Summary")
    st.write(df.describe())
else:
    st.info("Please upload a file to proceed.")
