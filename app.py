import streamlit as st
import pandas as pd
import plotly.express as px

file = st.file_uploader("Upload your CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    
    num_cols = df.select_dtypes(include=['number']).columns
    cat_cols = df.select_dtypes(include=['object']).columns

    choice = st.radio("What type of data do you want to analyze?", ("Numerical(Numbers)", "Categorical(Labels)"))

    if choice == "Numerical(Numbers)":
        if num_cols.empty:
            st.warning("No numerical columns found in the dataset.")
        else:
            selected_col = st.selectbox("Pick a number column", num_cols)
    else:
        if cat_cols.empty:
            st.warning("No categorical columns found in the dataset.")
        else:
            selected_col = st.selectbox("Pick a category column", cat_cols)