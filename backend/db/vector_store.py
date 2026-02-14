import os
import sqlite3
import numpy as np
import faiss
from datetime import datetime

DB_PATH = "memory.db"
INDEX_PATH = "index.faiss"
DIM = 384

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

# -------- FAISS --------
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = faiss.IndexFlatL2(DIM)


def add_memory(employee: str, topic: str, embedding):
    vector = np.array([embedding]).astype("float32")

    index.add(vector)
    faiss.write_index(index, INDEX_PATH)

    cursor.execute(
        "INSERT INTO knowledge (employee, topic, timestamp) VALUES (?, ?, ?)",
        (employee, topic, datetime.utcnow().isoformat())
    )
    conn.commit()


def search_memory(query_embedding, k=5):
    if index.ntotal == 0:
        return []

    vector = np.array([query_embedding]).astype("float32")
    distances, ids = index.search(vector, k)

    results = []
    for idx in ids[0]:
        if idx == -1:
            continue

        cursor.execute("SELECT employee, topic FROM knowledge WHERE id = ?", (idx + 1,))
        row = cursor.fetchone()
        if row:
            results.append(row)

    return results
