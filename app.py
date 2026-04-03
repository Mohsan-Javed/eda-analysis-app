import streamlit as st
import pandas as pd
import plotly.express as px

file = st.file_uploader("Upload your CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    
    num_cols = df.select_dtypes(include=['number']).columns
    cat_cols = df.select_dtypes(include=['object']).columns

    tab1, tab2, tab3 = st.tabs(["Data Overview", "Summary Stats", "Visualizations"])

    with tab1:
        st.write("# Data Overview")
        st.write("Number of rows:", df.shape[0])
        st.write("Number of columns:", df.shape[1])

        st.write("### Column Types")
        st.write("Numerical Columns:")
        st.table(num_cols)
        st.write("Categorical Columns:")
        st.table(cat_cols)

    with tab2:
        choice = st.radio(
            "What type of data would you like to explore?",
            ["Select an option", "Numerical(Numbers)", "Categorical(Labels)"],
            index=0
        )

        if choice == "Numerical(Numbers)":
            if num_cols.empty:
                st.warning("No numerical columns found in the dataset.")
            else:
                selected_col = st.selectbox("Pick a number column", num_cols)
                col1, col2, col3 = st.columns(3)

                col1.metric(label="Average", value=round(df[selected_col].mean(), 2))
                col2.metric(label="Min", value=round(df[selected_col].min(), 2))
                col3.metric(label="Max", value=round(df[selected_col].max(), 2))

        elif choice == "Categorical(Labels)":
            if cat_cols.empty:
                st.warning("No categorical columns found in the dataset.")
            else:
                selected_col = st.selectbox("Pick a category column", cat_cols)
                col1, col2 = st.columns(2)
                with col1:
                    col1.metric(label="Unique Values", value=df[selected_col].nunique())
                
                with col2:
                    st.write("**Most Frequent Value:**")
                    most_freq = df[selected_col].value_counts().head(5)
                    st.dataframe(most_freq)
        else:
            st.info("Please select an option to explore the data.")

    with tab3:
        choice = st.radio(
            "What visualization would you like to see?",
            ["Select an option", "Numerical(Numbers)", "Categorical(Labels)"],
            index=0
        )

        if choice == "Numerical(Numbers)":
            if num_cols.empty:
                st.warning("No numerical columns found in the dataset.")
            else:
                selected_col = st.selectbox("Pick a number column", num_cols)
                fig = px.histogram(df, x=selected_col, marginal="rug", nbins=30, title=f"Distribution of {selected_col}")
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",  # Transparent background for the plot area
                    
                    paper_bgcolor="black"      # Outer margin area
                )
                st.plotly_chart(fig)

        elif choice == "Categorical(Labels)":
            if cat_cols.empty:
                st.warning("No categorical columns found in the dataset.")
            else:
                selected_col = st.selectbox("Pick a category column", cat_cols)
                top10 =df[selected_col].value_counts().nlargest(10).reset_index()
                top10.columns = [selected_col, 'count']
                fig = px.bar(top10,x='count', y=selected_col, title=f"Value Counts of {selected_col}", orientation='h')
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",  # Transparent background for the plot area
                    paper_bgcolor="black"      # Outer margin area
                )
                st.plotly_chart(fig)
        else:
            st.info("Please select an option to explore the data.")