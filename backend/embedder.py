# embedder.py
import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODEL_NAME)


def get_embedding(text: str):
    if not text:
        return [0.0] * 384

    model = get_model()
    return model.encode(text).tolist()
