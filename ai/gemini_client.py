"""
Gemini Client
Handles communication with the Gemini API.
"""

import os

from dotenv import load_dotenv

from google import genai

from config import (
    GEMINI_MODEL,
)

load_dotenv()


class GeminiClient:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "Gemini API Key not found."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def ask(self, prompt):

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return response.text