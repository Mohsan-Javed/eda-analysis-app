# EDA Profiler

EDA Profiler automates Exploratory Data Analysis on any CSV dataset, 
providing instant insights on data quality, distributions, and feature 
relationships. Built for ML engineers, data scientists, and analysts 
who need to understand their data before modeling.

## Live Demo
[Click here to try it live](https://huggingface.co/spaces/Mohsan-Javed/eda-profiler)

## Key Features
1. Accepts any CSV file and automatically separates numerical and categorical columns
2. Data Overview: total rows, columns, duplicate count, missing values with percentages, and raw data preview
3. Summary Statistics: mean, median, min, max, and standard deviation for numerical columns
4. Visualizations: histogram with rug plot, box plot for outlier detection, correlation matrix, and bar charts for categorical columns
5. Download support for every insight, statistics as CSV and charts as interactive HTML

## Tech Stack
- **Language:** Python
- **Interface:** Streamlit
- **Visualization:** Plotly
- **Data Processing:** Pandas

## Local Installation
1. Clone the repository:
   git clone https://github.com/Mohsan-Javed/eda-profiler.git
2. Install dependencies:
   pip install -r requirements.txt
3. Run the application:
   streamlit run app.py
