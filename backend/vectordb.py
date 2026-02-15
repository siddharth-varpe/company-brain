import os
import json
import faiss
import numpy as np

DATA_DIR = "data"
INDEX_FILE = os.path.join(DATA_DIR, "index.faiss")
META_FILE = os.path.join(DATA_DIR, "meta.json")

DIM = 384  # embedding size

# ----------- strictness controls -----------
SIMILARITY_THRESHOLD = 0.55   # lower = stricter (0.25 very strict, 0.45 loose)
MIN_VALID_MATCHES = 2         # minimum evidence commits needed
TOP_K = 8


# ----------- load or create index ----------
if os.path.exists(INDEX_FILE):
    index = faiss.read_index(INDEX_FILE)
else:
    index = faiss.IndexFlatL2(DIM)

if os.path.exists(META_FILE):
    with open(META_FILE, "r") as f:
        meta = json.load(f)
else:
    meta = []


def save():
    os.makedirs(DATA_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "w") as f:
        json.dump(meta, f)


# ----------- add commit ----------
def add(vector, data):
    vec = np.array([vector]).astype("float32")
    index.add(vec)
    meta.append(data)
    save()


# ----------- search commits ----------
def search(query_vec):
    if index.ntotal == 0:
        return []

    vec = np.array([query_vec]).astype("float32")
    D, I = index.search(vec, TOP_K)

    valid_results = []

    for dist, idx in zip(D[0], I[0]):
        if idx == -1:
            continue

        # Reject weak semantic matches
        if dist > SIMILARITY_THRESHOLD:
            continue

        valid_results.append(meta[idx])

    # Not enough evidence → no expert exists
    if len(valid_results) < MIN_VALID_MATCHES:
        return []

    return valid_results
