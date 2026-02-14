import os
import sqlite3
import numpy as np
import faiss
from datetime import datetime

# Always store DB beside this file (VERY IMPORTANT for Render)
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "memory.db")
INDEX_PATH = os.path.join(BASE_DIR, "index.faiss")

DIM = 384  # embedding size


# ---------- SQLITE ----------
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


# ---------- FAISS ----------
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = faiss.IndexFlatL2(DIM)


def add_memory(employee: str, topic: str, embedding):
    embedding = np.array([embedding]).astype("float32")

    # store metadata
    cursor.execute(
        "INSERT INTO knowledge (employee, topic, timestamp) VALUES (?, ?, ?)",
        (employee, topic, str(datetime.utcnow()))
    )
    conn.commit()

    # store vector
    index.add(embedding)
    faiss.write_index(index, INDEX_PATH)


def search_memory(question_embedding, k=3):
    if index.ntotal == 0:
        return None

    question_embedding = np.array([question_embedding]).astype("float32")
    distances, indices = index.search(question_embedding, k)

    matches = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx == -1:
            continue

        cursor.execute("SELECT employee, topic FROM knowledge WHERE id=?", (idx + 1,))
        row = cursor.fetchone()
        if row:
            employee, topic = row
            similarity = 1 / (1 + dist)  # convert L2 distance to similarity
            matches.append((employee, similarity, topic))

    if not matches:
        return None

    # pick best employee
    best_employee = {}
    for emp, score, topic in matches:
        if emp not in best_employee:
            best_employee[emp] = [score, []]
        best_employee[emp][0] += score
        best_employee[emp][1].append(topic)

    employee = max(best_employee, key=lambda x: best_employee[x][0])
    score, topics = best_employee[employee]

    return employee, score, topics
