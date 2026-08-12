import pandas as pd
def load_csv(filepath):
    """
    Reads CSV and returns a Pandas DataFrame.
    """
    df = pd.read_csv(filepath)
    return df

def dataset_summary(df):
    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict()
    }
    return summary