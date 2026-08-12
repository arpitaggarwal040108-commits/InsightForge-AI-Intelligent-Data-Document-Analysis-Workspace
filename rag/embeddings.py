"""
Gemini Embedding Generator
"""

import os

from dotenv import load_dotenv
from google import genai

from config import EMBEDDING_MODEL

load_dotenv()


class EmbeddingGenerator:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "Gemini API key not found."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def embed(self, text):

        response = self.client.models.embed_content(

            model=EMBEDDING_MODEL,

            contents=text

        )

        return response.embeddings[0].values

    def embed_chunks(self, chunks):

        vectors = []

        for chunk in chunks:

            # If chunk is a dictionary (new format)
            if isinstance(chunk, dict):

                text = chunk["text"]

            else:
                # Backward compatibility
                text = chunk

            vectors.append(
                self.embed(text)
            )

        return vectors