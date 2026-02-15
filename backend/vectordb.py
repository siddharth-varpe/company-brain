import os
import json
import faiss
import numpy as np

DATA_DIR = "data"
INDEX_FILE = os.path.join(DATA_DIR, "index.faiss")
META_FILE = os.path.join(DATA_DIR, "meta.json")

DIM = 64  # MUST MATCH embedder

os.makedirs(DATA_DIR, exist_ok=True)


def create_new_index():
    return faiss.IndexFlatL2(DIM)


# load or rebuild safely
if os.path.exists(INDEX_FILE):
    try:
        index = faiss.read_index(INDEX_FILE)
        if index.d != DIM:
            raise Exception("dimension mismatch")
    except:
        index = create_new_index()
else:
    index = create_new_index()


if os.path.exists(META_FILE):
    with open(META_FILE, "r") as f:
        meta = json.load(f)
else:
    meta = []


def save():
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "w") as f:
        json.dump(meta, f)


def add(vector, data):
    vector = np.array([vector]).astype("float32")
    index.add(vector)
    meta.append(data)
    save()


def search(vector, k=3):
    if index.ntotal == 0:
        return []

    vector = np.array([vector]).astype("float32")
    D, I = index.search(vector, k)

    results = []
    for idx in I[0]:
        if idx < len(meta):
            results.append(meta[idx])
    return results
