"""
Builds context from uploaded CSV for Gemini.
"""

import pandas as pd


def build_csv_context(df: pd.DataFrame) -> str:
    """
    Creates a textual summary of the uploaded dataset.
    """

    context = []

    context.append("DATASET INFORMATION")
    context.append("=" * 50)

    context.append(f"Rows: {df.shape[0]}")
    context.append(f"Columns: {df.shape[1]}")

    context.append("")

    context.append("COLUMN NAMES")

    for column in df.columns:
        context.append(f"- {column}")

    context.append("")

    context.append("DATA TYPES")

    for column in df.columns:
        context.append(
            f"{column}: {df[column].dtype}"
        )

    context.append("")

    context.append("MISSING VALUES")

    for column in df.columns:
        context.append(
            f"{column}: {df[column].isnull().sum()}"
        )

    context.append("")

    context.append("FIRST FIVE ROWS")

    context.append(
        df.head().to_string(index=False)
    )

    context.append("")

    context.append("NUMERICAL SUMMARY")

    context.append(
        df.describe().to_string()
    )

    return "\n".join(context)