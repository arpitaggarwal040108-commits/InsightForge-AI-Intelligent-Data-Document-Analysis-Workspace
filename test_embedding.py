from rag.embeddings import EmbeddingGenerator

generator = EmbeddingGenerator()

vector = generator.embed(
    "Machine Learning is amazing."
)

print(len(vector))

print(vector[:10])