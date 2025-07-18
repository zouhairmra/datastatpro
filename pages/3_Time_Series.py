import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Time Series Analysis")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]
    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    datetime_column = st.selectbox("Select the datetime column", df.columns)
    value_column = st.selectbox("Select the value column", df.columns)

    df[datetime_column] = pd.to_datetime(df[datetime_column])
    df = df.sort_values(by=datetime_column)

    st.line_chart(df.set_index(datetime_column)[value_column])
    
    st.markdown("Use the plot above to visually explore trends and seasonality.")
else:
    st.info("Upload a dataset to start time series analysis.")
