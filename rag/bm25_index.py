"""
BM25 Index
Keyword-based retrieval.
"""

from rank_bm25 import BM25Okapi


class BM25Index:

    def __init__(self, chunks):

        self.chunks = chunks

        corpus = []

        for chunk in chunks:

            if isinstance(chunk, dict):
                corpus.append(
                    chunk["text"].lower().split()
                )
            else:
                corpus.append(
                    chunk.lower().split()
                )

        self.index = BM25Okapi(corpus)

    def search(self, question, top_k=3):

        tokens = question.lower().split()

        scores = self.index.get_scores(tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            idx
            for idx, score in ranked[:top_k]
        ]