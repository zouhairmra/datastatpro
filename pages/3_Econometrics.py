import streamlit as st
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, RandomEffects
from linearmodels.iv import GMM

st.title("📊 Econometric Modeling: Time Series & Panel Data")

uploaded_file = st.file_uploader("Upload a dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### 🔍 Data Preview:")
    st.dataframe(df.head())

    data_type = st.selectbox("Select the data structure:", ["Time Series", "Panel Data"])

    if data_type == "Time Series":
        df = df.dropna()
        columns = df.select_dtypes(include='number').columns.tolist()
        y = st.selectbox("Dependent variable:", columns)
        X = st.multiselect("Independent variables:", [col for col in columns if col != y])

        if X:
            model = sm.OLS(df[y], sm.add_constant(df[X])).fit()
            st.write("### OLS Results:")
            st.text(model.summary())

    elif data_type == "Panel Data":
        st.info("Your panel data must include columns for entity and time (e.g., firm, year).")
        entity = st.selectbox("Select entity identifier (e.g. firm):", df.columns)
        time = st.selectbox("Select time identifier (e.g. year):", df.columns)

        df_panel = df.set_index([entity, time])
        df_panel = df_panel.dropna()

        columns = df_panel.select_dtypes(include='number').columns.tolist()
        y = st.selectbox("Dependent variable:", columns, key="panel_y")
        X = st.multiselect("Independent variables:", [col for col in columns if col != y], key="panel_x")

        if X:
            estimation_type = st.radio("Estimation method:", ["Fixed Effects", "Random Effects", "GMM"])
            exog = sm.add_constant(df_panel[X])

            if estimation_type == "Fixed Effects":
                model = PanelOLS(df_panel[y], exog, entity_effects=True)
                results = model.fit()
                st.text(results.summary)

            elif estimation_type == "Random Effects":
                model = RandomEffects(df_panel[y], exog)
                results = model.fit()
                st.text(results.summary)

          
else:
    st.info("Please upload a dataset to begin analysis.")
