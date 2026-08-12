"""
PDF Loader
Extracts text using PyMuPDF.
"""

import fitz

import fitz


def extract_text(pdf_path):

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):

        pages.append(
            {
                "page": page_number + 1,
                "text": page.get_text()
            }
        )

    document.close()

    return pages