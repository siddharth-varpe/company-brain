import os
import sqlite3
import numpy as np
import faiss
from datetime import datetime

DB_PATH = "memory.db"
INDEX_PATH = "index.faiss"
DIM = 384  # embedding size

# ---------- SQLITE (metadata storage) ----------

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee TEXT,
    topic TEXT,
    timestamp TEXT
)
""")
conn.commit()


# ---------- FAISS (embedding search) ----------

if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = faiss.IndexFlatL2(DIM)


def save_index():
    faiss.write_index(index, INDEX_PATH)


# ---------- ADD MEMORY ----------

def add_memory(employee: str, topic: str, embedding):

    # store metadata
    cursor.execute(
        "INSERT INTO knowledge (employee, topic, timestamp) VALUES (?, ?, ?)",
        (employee, topic, datetime.now().isoformat())
    )
    conn.commit()

    # store vector
    vector = np.array([embedding]).astype("float32")
    index.add(vector)

    save_index()


# ---------- SEARCH MEMORY ----------

def search_memory(query_embedding, k=10):

    if index.ntotal == 0:
        return []

    query = np.array([query_embedding]).astype("float32")
    distances, ids = index.search(query, k)

    results = []

    for dist, idx in zip(distances[0], ids[0]):
        if idx == -1:
            continue

        cursor.execute("SELECT employee, topic, timestamp FROM knowledge WHERE id=?", (int(idx+1),))
        row = cursor.fetchone()

        if row:
            results.append({
                "employee": row[0],
                "topic": row[1],
                "timestamp": row[2],
                "distance": float(dist)   # <-- NEW
            })

    return results
