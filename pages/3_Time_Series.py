import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📈 Time Series Analysis & Exploratory Data Analysis")

uploaded_file = st.file_uploader("Upload a time series dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### 🔍 Data Preview")
    st.dataframe(df.head())

    date_col = st.selectbox("Select the datetime column", df.columns)
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    value_col = st.selectbox("Select a numeric variable to analyze", numeric_cols)

    try:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(by=date_col)
        df.set_index(date_col, inplace=True)

        st.write("### 📊 Time Series Line Plot")
        fig, ax = plt.subplots()
        ax.plot(df[value_col])
        ax.set_title(f"Time Series Plot of {value_col}")
        ax.set_xlabel("Date")
        ax.set_ylabel(value_col)
        st.pyplot(fig)

        st.write("### 🔍 Scatter Plot")
        other_col = st.selectbox("Select another numeric variable for scatter plot", [col for col in numeric_cols if col != value_col])
        fig2, ax2 = plt.subplots()
        ax2.scatter(df[value_col], df[other_col])
        ax2.set_xlabel(value_col)
        ax2.set_ylabel(other_col)
        ax2.set_title(f"Scatter Plot: {value_col} vs {other_col}")
        st.pyplot(fig2)

        st.write("### 📈 Histogram")
        bins = st.slider("Number of bins for histogram", 5, 100, 20)
        fig3, ax3 = plt.subplots()
        ax3.hist(df[value_col], bins=bins, color='skyblue', edgecolor='black')
        ax3.set_title(f"Histogram of {value_col}")
        st.pyplot(fig3)

        st.write("### 🔗 Correlation Matrix Heatmap")
        corr = df[numeric_cols].corr()
        fig4, ax4 = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax4)
        st.pyplot(fig4)

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Please upload a time series dataset to begin.")
