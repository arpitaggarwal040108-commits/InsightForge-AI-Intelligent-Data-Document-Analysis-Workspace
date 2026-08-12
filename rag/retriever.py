"""
Retriever
Searches the FAISS index for relevant chunks.
"""

import numpy as np


class Retriever:

    def __init__(self, embedder, index, chunks):

        self.embedder = embedder
        self.index = index
        self.chunks = chunks

    def retrieve(self, question, top_k=2):

        # Create embedding for question
        vector = self.embedder.embed(question)
        vector = np.array([vector], dtype=np.float32)

        # Search FAISS
        distances, indices = self.index.search(
            vector,
            top_k
        )

        results = []

        seen = set()

        for idx in indices[0]:

            if idx == -1:
                continue

            if idx >= len(self.chunks):
                continue

            chunk = self.chunks[idx]

            # New format (dictionary)
            if isinstance(chunk, dict):

                text = chunk["text"]

                if not text.strip():
                    continue

                if text in seen:
                    continue

                seen.add(text)

                results.append({
                    "text": text,
                    "page": chunk["page"],
                    "chunk_id": chunk["chunk_id"]
                })

            # Old format (string)
            else:

                text = chunk.strip()

                if not text:
                    continue

                if text in seen:
                    continue

                seen.add(text)

                results.append({
                    "text": text,
                    "page": None,
                    "chunk_id": None
                })

        return results