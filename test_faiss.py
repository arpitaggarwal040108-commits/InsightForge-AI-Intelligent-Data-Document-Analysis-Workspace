from rag.faiss_index import FAISSIndex
import numpy as np

vectors = np.random.rand(
    10,
    128
).astype("float32")

index = FAISSIndex(128)

index.add_vectors(vectors)

print(index.index.ntotal)
