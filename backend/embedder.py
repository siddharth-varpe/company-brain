from sentence_transformers import SentenceTransformer
import numpy as np
import torch
import os

# Prevent tokenizer multi-thread RAM explosion
os.environ["TOKENIZERS_PARALLELISM"] = "false"

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )
        _model.max_seq_length = 256
    return _model


def get_embedding(text: str) -> np.ndarray:
    if not text or not text.strip():
        return np.zeros(384, dtype="float32")

    model = get_model()

    with torch.no_grad():
        vec = model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )

    return vec.astype("float32")
