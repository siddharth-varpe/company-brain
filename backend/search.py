from collections import Counter
from backend.embedder import get_embedding
from backend.vectordb import search

def ask_brain(question: str):
    vec = get_embedding(question)
    results = search(vec, k=15)   # fetch more for accuracy

    if not results:
        return ["No expert found yet"]

    # count expertise
    scores = Counter()
    for r in results:
        scores[r["author"]] += 1

    # rank experts
    top = scores.most_common(3)

    response = []
    for i, (name, score) in enumerate(top, start=1):
        response.append(f"{i}. {name} (confidence {score})")

    return response
