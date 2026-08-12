"""
Hybrid Retriever
Combines FAISS + BM25.
"""

import numpy as np

from rag.bm25_index import BM25Index


class HybridRetriever:

    def __init__(self, embedder, faiss_index, chunks):

        self.embedder = embedder
        self.faiss = faiss_index
        self.chunks = chunks

        self.bm25 = BM25Index(chunks)

    def retrieve(self, question, top_k=3):

        # ---------- FAISS ----------

        vector = self.embedder.embed(question)

        vector = np.array(
            [vector],
            dtype=np.float32
        )

        _, faiss_indices = self.faiss.search(
            vector,
            top_k
        )

        faiss_indices = list(faiss_indices[0])

        # ---------- BM25 ----------

        bm25_indices = self.bm25.search(
            question,
            top_k
        )

        # ---------- Merge ----------

        merged = []

        seen = set()

        for idx in faiss_indices + bm25_indices:

            if idx == -1:
                continue

            if idx in seen:
                continue

            seen.add(idx)

            merged.append(
                self.chunks[idx]
            )

        return merged
    