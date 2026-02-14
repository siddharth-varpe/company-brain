from backend.embedder import get_embedding
from backend.db.vector_store import search

def find_expert(question: str):
    emb = get_embedding(question)
    result = search(emb)

    if not result:
        return "No expert found yet."

    employee, topic = result
    return f"{employee} knows about: {topic}"
