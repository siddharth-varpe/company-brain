import hashlib
import numpy as np

DIM = 64

def get_embedding(text: str):
    h = hashlib.sha256(text.encode()).hexdigest()

    needed = DIM * 2
    while len(h) < needed:
        h += h

    vec = [int(h[i:i+2], 16)/255 for i in range(0, needed, 2)]

    return np.array(vec, dtype="float32")
