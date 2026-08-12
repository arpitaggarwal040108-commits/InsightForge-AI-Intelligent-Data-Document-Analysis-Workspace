"""
FAISS Index Manager
"""

import os
import faiss
import numpy as np


class FAISSIndex:

    def __init__(self, dimension):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(
            dimension
        )

    def add_vectors(self, vectors):

        vectors = np.array(
            vectors,
            dtype=np.float32
        )

        self.index.add(vectors)

    def save(self, filepath):

        folder = os.path.dirname(filepath)

        os.makedirs(folder, exist_ok=True)

        faiss.write_index(
            self.index,
            filepath
        )

    @staticmethod
    def load(filepath):

        return faiss.read_index(
            filepath
        )