import streamlit as st
import pandas as pd
import statsmodels.api as sm

st.title("📊 Econometric Modeling")

uploaded_file = st.file_uploader("Upload a dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### 🔍 Data Preview:")
    st.dataframe(df.head())

    columns = df.select_dtypes(include='number').columns.tolist()
    if len(columns) < 2:
        st.warning("Need at least one dependent and one independent variable.")
    else:
        y = st.selectbox("Select the dependent variable (Y):", columns)
        X = st.multiselect("Select independent variables (X):", [col for col in columns if col != y])

        if X:
            model = sm.OLS(df[y], sm.add_constant(df[X])).fit()
            st.write("### 📑 Regression Results")
            st.text(model.summary())
        else:
            st.info("Select at least one X variable.")
else:
    st.info("Please upload a dataset to run regression.")
