import pandas as pd

def remove_duplicates(df):
    """
    Removes duplicate rows.
    """
    return df.drop_duplicates()

def remove_empty_rows(df):
    """
    Removes rows where every value is empty.
    """
    return df.dropna(how="all")

def fill_numeric_missing(df):
    """
    Fill numeric missing values with column mean.
    """
    numeric_columns = df.select_dtypes(include="number").columns
    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].mean())
    return df


def fill_categorical_missing(df):
    """
    Fill text columns with 'Unknown'.
    """
    categorical_columns = df.select_dtypes(include="object").columns
    for column in categorical_columns:
        df[column] = df[column].fillna("Unknown")
    return df

def strip_spaces(df):
    """
    Remove extra spaces from text columns.
    """
    object_columns = df.select_dtypes(include="object").columns
    for column in object_columns:
        df[column] = df[column].str.strip()

    return df
def clean_dataset(df):
    """
    Complete cleaning pipeline.
    """
    df = remove_duplicates(df)
    df = remove_empty_rows(df)
    df = strip_spaces(df)
    df = fill_numeric_missing(df)
    df = fill_categorical_missing(df)
    return df