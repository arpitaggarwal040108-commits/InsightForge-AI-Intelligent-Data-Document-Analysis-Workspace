import os
import matplotlib.pyplot as plt
import numpy as np

def create_visualizations(df, chart_folder):
    """
    Generates charts from numerical columns.

    Returns dictionary of image filenames.
    """
    charts = {}

    numeric_columns = df.select_dtypes(include=np.number).columns

    if len(numeric_columns) == 0:
        return charts

    # ---------------- Histogram ----------------

    column = numeric_columns[0]

    plt.figure(figsize=(6,4))

    plt.hist(df[column], bins=10)

    plt.title(f"{column} Histogram")

    plt.xlabel(column)

    plt.ylabel("Frequency")

    histogram_path = os.path.join(chart_folder, "histogram.png")

    plt.savefig(histogram_path)

    plt.close()

    charts["histogram"] = "charts/histogram.png"

    # ---------------- Box Plot ----------------

    plt.figure(figsize=(6,4))

    plt.boxplot(df[column])

    plt.title(f"{column} Box Plot")

    boxplot_path = os.path.join(chart_folder, "boxplot.png")

    plt.savefig(boxplot_path)

    plt.close()

    charts["boxplot"] = "charts/boxplot.png"

    # ---------------- Bar Chart ----------------

    plt.figure(figsize=(6,4))

    df[column].head(10).plot(kind="bar")

    plt.title(f"{column} Bar Chart")

    bar_path = os.path.join(chart_folder, "bar.png")

    plt.savefig(bar_path)

    plt.close()

    charts["bar"] = "charts/bar.png"

    # ---------------- Line Chart ----------------

    plt.figure(figsize=(6,4))

    df[column].head(20).plot(kind="line")

    plt.title(f"{column} Line Chart")

    line_path = os.path.join(chart_folder, "line.png")

    plt.savefig(line_path)

    plt.close()

    charts["line"] = "charts/line.png"

    # ---------------- Scatter Plot ----------------

    if len(numeric_columns) >= 2:

        x = numeric_columns[0]

        y = numeric_columns[1]

        plt.figure(figsize=(6,4))

        plt.scatter(df[x], df[y])

        plt.xlabel(x)

        plt.ylabel(y)
        plt.title(f"{x} vs {y}")
        scatter_path = os.path.join(chart_folder, "scatter.png")
        plt.savefig(scatter_path)
        plt.close()
        charts["scatter"] = "charts/scatter.png"
    return charts