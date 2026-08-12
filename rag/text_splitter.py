"""
Text Splitter
Splits PDF pages into overlapping chunks while preserving page numbers.
"""

import re


def split_text(
    pages,
    chunk_size=500,
    overlap=100
):
    """
    Parameters
    ----------
    pages : list[dict]

    Example:
    [
        {
            "page": 1,
            "text": "...."
        }
    ]

    Returns
    -------
    list[dict]

    Example:

    [
        {
            "text": "...",
            "page": 1,
            "chunk_id": 0
        }
    ]
    """

    chunks = []

    chunk_id = 0

    for page_data in pages:

        page_number = page_data["page"]

        text = re.sub(
            r"\s+",
            " ",
            page_data["text"]
        ).strip()

        start = 0

        text_length = len(text)

        while start < text_length:

            end = min(
                start + chunk_size,
                text_length
            )

            chunk = text[start:end]

            if end < text_length:

                last_period = chunk.rfind(".")

                last_newline = chunk.rfind("\n")

                boundary = max(
                    last_period,
                    last_newline
                )

                if boundary > chunk_size * 0.6:

                    end = start + boundary + 1

                    chunk = text[start:end]

            chunks.append({

                "document": None,

                "text": chunk.strip(),

                "page": page_number,

                "chunk_id": chunk_id

            })
            chunk_id += 1

            if end == text_length:
                break

            start = max(
                end - overlap,
                0
            )

    return chunks