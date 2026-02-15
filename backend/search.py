from backend.embedder import get_embedding
from backend.vectordb import search

def ask_brain(question: str):
    vec = get_embedding(question)
    results = search(vec)

    if not results:
        return "I don't know yet."

    answer = "\n".join([f"{r['author']}: {r['message']}" for r in results])
    return answer
