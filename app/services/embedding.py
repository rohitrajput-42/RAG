from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str) -> np.ndarray:
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding