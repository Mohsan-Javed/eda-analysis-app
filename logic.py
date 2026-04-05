import pandas as pd

def get_recommendations(df, col):
    recs = []
    
    # 1. Calculate the necessary metrics
    missing_pct = (df[col].isnull().sum() / len(df)) * 100
    
    # 2. Check for Numerical specific issues
    if pd.api.types.is_numeric_dtype(df[col]):
        skewness = df[col].skew()
        if abs(skewness) > 1:
            recs.append(f"The column '{col}' is highly skewed (skewness: {skewness:.2f}). Consider applying a log transformation to reduce skewness and then perform median imputation.")
            # Add logic for outliers here...
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            if not outliers.empty:
                recs.append(f"The column '{col}' contains outliers. Consider removing or treating them.")
        else:
            recs.append(f"The column '{col}' has a skewness of {skewness:.2f}, which is within an acceptable range. Consider using mean imputation for missing values.")
            z = (df[col] - df[col].mean()) / df[col].std()
            outliers = df[abs(z) > 3]
            if not outliers.empty:
                recs.append(f"The column '{col}' contains outliers. Investigate if these are data errors. If they are valid extreme values, consider Capping (Winsorization) to the 99th percentile.")

    # 3. Check for Missing Values (using your 4-tier logic)
    if missing_pct > 0:
        if missing_pct <= 5:
            recs.append(f"The column '{col}' has {missing_pct:.2f}% missing values. Consider using simple imputation or dropping the missing values.")
        elif missing_pct >= 5 and missing_pct <= 50:
            recs.append(f"The column '{col}' has {missing_pct:.2f}% missing values. Consider using mean imputation if the data is normally distributed and median imputation if it is not.")
        elif missing_pct > 50 and missing_pct <= 80:
            recs.append(f"The column '{col}' has {missing_pct:.2f}% missing values. Consider adding a missing indicator column.")
        else:
            recs.append(f"The column '{col}' has {missing_pct:.2f}% missing values. Consider dropping the column as it may not provide much useful information.")
    
    #4 Check for multicollinearity (for numerical columns)
    if pd.api.types.is_numeric_dtype(df[col]):
        corr_matrix = df.select_dtypes(include='number').corr()
        high_corr = corr_matrix[abs(corr_matrix[col]) > 0.9][col].index.tolist()
        high_corr.remove(col)  # Remove the column itself from the list
        if high_corr:
            recs.append(f"The column '{col}' is highly correlated with {', '.join(high_corr)}. Consider dropping one of the correlated columns to reduce multicollinearity.")
    return recs
