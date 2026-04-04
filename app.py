import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(file):
    return pd.read_csv(file)


file = st.file_uploader("Upload your CSV file", type=["csv"])

if file is not None:

    df = load_data(file)

    num_cols = df.select_dtypes(include=['number']).columns
    cat_cols = df.select_dtypes(include=['object']).columns

    st.sidebar.title("Project Settings")

    choice = st.sidebar.radio(
            "What type of data would you like to explore?",
            ["Select an option", "Numerical(Numbers)", "Categorical(Labels)"],
            index=0
        )
    if choice == "Select an option":
        st.header("Welcome to the EDA Tool")
        st.caption("Please select a data type from the sidebar to explore your dataset.")
        st.caption("Then pick a specific column to see summary statistics and visualizations.")
        st.caption("Then use the tabs to navigate between data overview, summary stats, and visualizations.")

    elif choice == "Categorical(Labels)":
        selected_col = st.sidebar.selectbox("Pick a category column", cat_cols)
    elif choice == "Numerical(Numbers)":
        selected_col = st.sidebar.selectbox("Pick a number column", num_cols)

    tab1, tab2, tab3 = st.tabs(["Data Overview", "Summary Stats", "Visualizations"])

    if choice != "Numerical(Numbers)" and choice != "Categorical(Labels)":
        st.info("Please select an option to explore the data.")

    elif choice != "Select an option":
        with tab1:

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Number of rows:", df.shape[0])
            with col2:
                st.metric("Number of columns:", df.shape[1])
            with col3:
                st.metric("Duplicate rows:", df.duplicated().sum())

            null_count = df.isnull().sum()

            if null_count.empty or null_count.sum() == 0:
                st.success("No missing values found in the dataset.")
            else:
                null_count_perc = (null_count / df.shape[0]) * 100
                null_count = null_count[null_count > 0]
                null_count = null_count.reset_index()
                null_count.columns = ["Column Name", "Missing Values"]
                null_count["Percentage Missing"] = round((null_count["Missing Values"] / df.shape[0]) * 100, 2)
                null_count = null_count.sort_values(by="Missing Values", ascending=False)
                st.text("Columns with missing values:")
                st.table(null_count)

            st.text("Raw Data Preview:")
            st.dataframe(df.sample(10))

        with tab2:

            if choice == "Numerical(Numbers)":
                if num_cols.empty:
                    st.warning("No numerical columns found in the dataset.")
                else:
                    stats = df[selected_col].describe()
                    stats = stats.reset_index()
                    stats.columns = ["Statistic", "Value"]
                    st.dataframe(stats)

                    stats_csv = stats.to_csv(index=False)
                    st.download_button(
                        label="Download Summary Statistics as CSV",
                        data=stats_csv,
                        file_name=f"{selected_col}_summary_stats.csv")

            elif choice == "Categorical(Labels)":
                if cat_cols.empty:
                    st.warning("No categorical columns found in the dataset.")
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        col1.metric(label="Unique Values", value=df[selected_col].nunique())
                        
                    with col2:
                        st.write("**Most Frequent Value:**")
                        most_freq = df[selected_col].value_counts().head(5)
                        st.dataframe(most_freq)

        with tab3:
                
            if choice == "Numerical(Numbers)":
                if num_cols.empty:
                    st.warning("No numerical columns found in the dataset.")
                else:
                    st.header("Distribution Plot")
                    fig = px.histogram(df, x=selected_col, marginal="rug", nbins=30)
                    st.plotly_chart(fig)

                    charts_html = fig.to_html(full_html=True)
                    st.download_button(
                    label="Download Distribution Plot as HTML",
                    data=charts_html,
                    file_name=f"{selected_col}_distribution_plot.html")

                    st.header("Box Plot")
                    fig2 = px.box(df, y=selected_col)
                    st.plotly_chart(fig2)
                    charts_html2 = fig2.to_html(full_html=True)
                    st.download_button(
                    label="Download Box Plot as HTML",
                    data=charts_html2,
                    file_name=f"{selected_col}_box_plot.html")

                    st.header("Correlation Matrix")
                    if num_cols.shape[0] > 1:
                        corr_matrix = df[num_cols].corr()
                        fig3 = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdBu_r')
                        st.plotly_chart(fig3)
                        charts_html3 = fig3.to_html(full_html=True)
                        st.download_button(
                            label="Download Correlation Matrix as HTML",
                            data=charts_html3,
                            file_name=f"{selected_col}_correlation_matrix.html"
                        )
                    else:
                        st.warning("Not enough numerical columns to compute correlation matrix.")

            elif choice == "Categorical(Labels)":
                if cat_cols.empty:
                    st.warning("No categorical columns found in the dataset.")
                else:
                    st.header("Value Counts")
                    top10 = df[selected_col].value_counts().nlargest(10).reset_index()
                    top10.columns = [selected_col, 'count']
                    fig = px.bar(top10,x='count', y=selected_col, orientation='h')
                    st.plotly_chart(fig)
                    charts_html = fig.to_html(full_html=True)
                    st.download_button(
                        label="Download Value Counts as HTML",
                        data=charts_html,
                        file_name=f"{selected_col}_value_counts.html"
                    )