from collections import Counter
from .embedder import get_embedding
from .db.vector_store import search_memory


def find_expert(question: str):

    embedding = get_embedding(question)
    memories = search_memory(embedding)

    if not memories:
        return {
            "expert": "Unknown",
            "reason": "No one in company has worked on this yet",
            "evidence": []
        }

    employees = [emp for emp, _ in memories]
    topics = [topic for _, topic in memories]

    best_employee = Counter(employees).most_common(1)[0][0]

    related_topics = [t for e, t in memories if e == best_employee]

    return {
        "expert": best_employee,
        "reason": "Has solved similar issues in the past",
        "evidence": related_topics[:5]
    }
