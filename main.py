import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="DatastatPro Clone",
    page_icon="📊",
    layout="wide",
)

# Display logo
logo = Image.open("logo.png")
st.image(logo, width=150)

# Main title and description
st.title("Welcome to DatastatPro Clone")
st.markdown("""
This is the homepage of your interactive economic & financial analytics app.

Use the **sidebar** to navigate through the tools. Available tools include:

- [📤 Upload Data](Upload_Data)
- [📈 Time Series Analysis](Time_Series)
- [📊 Econometric Modeling](Econometrics)
- [📬 Contact](Contact)

Explore datasets, perform modeling, and visualize your findings interactively!
""")
