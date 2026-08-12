"""
Natural Language DataFrame Agent
"""

import pandas as pd


class DataFrameAgent:

    def __init__(self, dataframe):
        self.df = dataframe

    def find_column(self, question):

        question = question.lower()

        for column in self.df.columns:

            if column.lower() in question:
                return column

        return None

    def find_number(self, question):

        words = question.split()

        for word in words:

            try:
                return float(word)
            except:
                pass

        return None

    def find_group_column(self, question):

        question = question.lower()

        if "by" not in question:
            return None

        after = question.split("by")[-1].strip()

        for column in self.df.columns:

            if column.lower() == after:
                return column

        return None

    def answer(self, question):

        question = question.lower()

        column = self.find_column(question)

        group_column = self.find_group_column(question)

        number = self.find_number(question)

        # ==========================
        # Dataset Information
        # ==========================

        if "rows" in question:

            return f"Rows: {len(self.df)}"

        if "columns" in question:

            return "\n".join(self.df.columns)

        if "shape" in question:

            return str(self.df.shape)

        if "duplicate" in question:

            return f"Duplicate rows: {self.df.duplicated().sum()}"

        if "missing" in question:

            return self.df.isnull().sum().to_string()

        # ==========================
        # Statistics
        # ==========================

        if column:

            if "average" in question or "mean" in question:

                return self.df[column].mean()

            if "median" in question:

                return self.df[column].median()

            if "maximum" in question or "max" in question:

                return self.df[column].max()

            if "minimum" in question or "min" in question:

                return self.df[column].min()

            if "standard deviation" in question:

                return self.df[column].std()

            if "variance" in question:

                return self.df[column].var()

            if "sum" in question:

                return self.df[column].sum()

            if "count" in question:

                return self.df[column].count()

            if "unique" in question:

                return self.df[column].nunique()

            if "value counts" in question:

                return self.df[column].value_counts().to_string()

        # ==========================
        # Top Rows
        # ==========================

        if "top" in question and column:

            n = int(number) if number else 5

            return self.df.sort_values(
                by=column,
                ascending=False
            ).head(n).to_string(index=False)

        # ==========================
        # Bottom Rows
        # ==========================

        if "bottom" in question and column:

            n = int(number) if number else 5

            return self.df.sort_values(
                by=column,
                ascending=True
            ).head(n).to_string(index=False)

        # ==========================
        # Highest Row
        # ==========================

        if "highest" in question and column:

            row = self.df.loc[
                self.df[column].idxmax()
            ]

            return row.to_string()

        # ==========================
        # Lowest Row
        # ==========================

        if "lowest" in question and column:

            row = self.df.loc[
                self.df[column].idxmin()
            ]

            return row.to_string()

        # ==========================
        # Sort Ascending
        # ==========================

        if "ascending" in question and column:

            return self.df.sort_values(
                by=column
            ).to_string(index=False)

        # ==========================
        # Sort Descending
        # ==========================

        if "descending" in question and column:

            return self.df.sort_values(
                by=column,
                ascending=False
            ).to_string(index=False)

        # ==========================
        # GroupBy Mean
        # ==========================

        if column and group_column:

            if "average" in question or "mean" in question:

                return self.df.groupby(
                    group_column
                )[column].mean().to_string()

        # ==========================
        # GroupBy Maximum
        # ==========================

        if column and group_column:

            if "maximum" in question:

                return self.df.groupby(
                    group_column
                )[column].max().to_string()

        # ==========================
        # GroupBy Minimum
        # ==========================

        if column and group_column:

            if "minimum" in question:

                return self.df.groupby(
                    group_column
                )[column].min().to_string()

        # ==========================
        # Filtering
        # ==========================

        if column and ">=" in question and number is not None:

            return self.df[
                self.df[column] >= number
            ].to_string(index=False)

        if column and "<=" in question and number is not None:

            return self.df[
                self.df[column] <= number
            ].to_string(index=False)

        if column and ">" in question and number is not None:

            return self.df[
                self.df[column] > number
            ].to_string(index=False)

        if column and "<" in question and number is not None:

            return self.df[
                self.df[column] < number
            ].to_string(index=False)

        # ==========================
        # Correlation
        # ==========================

        if "correlation" in question:

            return self.df.corr(
                numeric_only=True
            ).to_string()

        # ==========================
        # Head
        # ==========================

        if "head" in question:

            return self.df.head().to_string(index=False)

        # ==========================
        # Tail
        # ==========================

        if "tail" in question:

            return self.df.tail().to_string(index=False)

        return None