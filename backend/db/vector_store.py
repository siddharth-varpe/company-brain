import sqlite3
import json
import math

DB_PATH = "memory.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee TEXT,
        topic TEXT,
        embedding TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_memory(employee, topic, embedding):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO memory (employee, topic, embedding) VALUES (?, ?, ?)",
        (employee, topic, json.dumps(embedding))
    )

    conn.commit()
    conn.close()


def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    mag1 = math.sqrt(sum(x*x for x in a))
    mag2 = math.sqrt(sum(x*x for x in b))
    return dot / (mag1 * mag2 + 1e-8)


def search(query_embedding):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT employee, topic, embedding FROM memory")
    rows = c.fetchall()

    conn.close()

    best = None
    best_score = -1

    for employee, topic, emb in rows:
        emb = json.loads(emb)
        score = cosine(query_embedding, emb)
        if score > best_score:
            best_score = score
            best = (employee, topic)

    return best
