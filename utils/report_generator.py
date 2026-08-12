"""
Report Generator
Generates PDF reports for dataset analysis.
"""

import os

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_report(
    filepath,
    summary,
    statistics
):
    """
    Generate a PDF report.
    """

    document = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    elements = []

    # -------------------------
    # Title
    # -------------------------

    elements.append(
        Paragraph(
            "Smart AI Data Explorer Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    # -------------------------
    # Dataset Summary
    # -------------------------

    elements.append(
        Paragraph(
            "Dataset Summary",
            styles["Heading2"]
        )
    )

    summary_table = [

        ["Property", "Value"],

        ["Rows", str(summary["rows"])],

        ["Columns", str(summary["columns"])],

        [
            "Missing Values",
            str(summary["missing_values"])
        ]

    ]

    table = Table(summary_table)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 12)

        ])

    )

    elements.append(table)

    elements.append(
        Spacer(1, 20)
    )

    # -------------------------
    # Statistics
    # -------------------------

    elements.append(
        Paragraph(
            "Numerical Statistics",
            styles["Heading2"]
        )
    )

    for column, values in statistics.items():

        elements.append(

            Paragraph(
                f"<b>{column}</b>",
                styles["Heading3"]
            )

        )

        stats_table = [

            ["Metric", "Value"],

            ["Mean", str(values["mean"])],

            ["Median", str(values["median"])],

            ["Mode", str(values["mode"])],

            ["Standard Deviation", str(values["std"])],

            ["Variance", str(values["variance"])],

            ["Minimum", str(values["minimum"])],

            ["Maximum", str(values["maximum"])]

        ]

        table = Table(stats_table)

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey)

            ])

        )

        elements.append(table)

        elements.append(
            Spacer(1, 15)
        )

    document.build(elements)