import faiss
import json
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

INDEX_PATH = os.path.join(DATA_DIR, "index.faiss")
META_PATH = os.path.join(DATA_DIR, "meta.json")

DIM = 384

index = None
metadata = []


def load():
    global index, metadata

    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
    else:
        index = faiss.IndexFlatL2(DIM)

    if os.path.exists(META_PATH):
        with open(META_PATH, "r") as f:
            metadata = json.load(f)
    else:
        metadata = []


def save():
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w") as f:
        json.dump(metadata, f, indent=2)


def add(vector, data):
    global index, metadata

    if index is None:
        load()

    vector = np.array([vector]).astype("float32")
    index.add(vector)

    metadata.append(data)

    save()


def get_all():
    if index is None:
        load()
    return metadata
