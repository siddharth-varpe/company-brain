from sentence_transformers import SentenceTransformer
import numpy as np
import os

# Lazy load (critical for 512MB RAM)
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_embedding(text: str) -> np.ndarray:
    model = get_model()

    vec = model.encode(
        text,
        normalize_embeddings=True,   # makes cosine similarity reliable
        show_progress_bar=False
    )

    return np.array(vec, dtype="float32")
