import os
import json
import faiss
import numpy as np

DATA_DIR = "data"
INDEX_FILE = os.path.join(DATA_DIR, "index.faiss")
META_FILE = os.path.join(DATA_DIR, "meta.json")

DIM = 64  # MUST match embedder

os.makedirs(DATA_DIR, exist_ok=True)

# ---------- LOAD OR CREATE INDEX ----------
if os.path.exists(INDEX_FILE):
    try:
        index = faiss.read_index(INDEX_FILE)
    except:
        index = faiss.IndexFlatL2(DIM)
else:
    index = faiss.IndexFlatL2(DIM)

# ---------- LOAD META ----------
if os.path.exists(META_FILE):
    try:
        with open(META_FILE, "r") as f:
            meta = json.load(f)
    except:
        meta = []
else:
    meta = []

# ---------- SAVE ----------
def save():
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "w") as f:
        json.dump(meta, f)

# ---------- ADD ----------
def add(vector, data):
    vector = np.array([vector]).astype("float32")
    index.add(vector)
    meta.append(data)
    save()

# ---------- SEARCH ----------
def search(query_vector, k=3):
    if index.ntotal == 0:
        return []

    query_vector = np.array([query_vector]).astype("float32")
    distances, ids = index.search(query_vector, k)

    results = []
    for i in ids[0]:
        if i < len(meta):
            results.append(meta[i])
    return results
