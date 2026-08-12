import pandas as pd
import numpy as np


def numerical_summary(df):
    """
    Returns statistical summary for all numerical columns.
    """
    numeric_df = df.select_dtypes(include=np.number)
    summary = {}
    for column in numeric_df.columns:
        mode = numeric_df[column].mode()
        summary[column] = {
            "count": int(numeric_df[column].count()),
            "mean": round(numeric_df[column].mean(), 2),
            "median": round(numeric_df[column].median(), 2),
            "mode": mode.iloc[0] if not mode.empty else "N/A",
            "std": round(numeric_df[column].std(), 2),
            "variance": round(numeric_df[column].var(), 2),
            "minimum": numeric_df[column].min(),
            "maximum": numeric_df[column].max(),
            "sum": round(numeric_df[column].sum(), 2)
        }
    return summary

def categorical_summary(df):
    """
    Returns statistics for categorical columns.
    """
    categorical_df = df.select_dtypes(include="object")
    summary = {}
    for column in categorical_df.columns:
        mode = categorical_df[column].mode()
        summary[column] = {
            "count": int(categorical_df[column].count()),
            "unique": int(categorical_df[column].nunique()),
            "mode": mode.iloc[0] if not mode.empty else "N/A"
        }
    return summary

def correlation_matrix(df):
    """
    Returns correlation matrix of numerical columns.
    """
    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.shape[1] < 2:
        return pd.DataFrame()
    return numeric_df.corr().round(2)

def unique_values(df):
    """
    Returns number of unique values in every column.
    """
    unique = {}
    for column in df.columns:
        unique[column] = int(df[column].nunique())
    return unique

def dataset_overview(df):
    """
    Returns basic information about the dataset.
    """
    overview = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage_kb": round(df.memory_usage(deep=True).sum() / 1024, 2)
    }
    return overview