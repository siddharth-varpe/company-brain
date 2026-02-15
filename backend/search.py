from collections import Counter
from backend.embedder import get_embedding
from backend.vectordb import search


def ask_brain(question: str):
    vec = get_embedding(question)
    results = search(vec)

    # -------- no expert ----------
    if not results:
        return {
            "status": "no_expert",
            "message": "No relevant expert found for this issue yet."
        }

    # -------- count authors ----------
    author_counter = Counter()
    for r in results:
        author_counter[r["author"]] += 1

    # best expert
    best_author, best_count = author_counter.most_common(1)[0]

    # other contacts
    others = [a for a, _ in author_counter.most_common()[1:3]]

    return {
        "status": "expert_found",
        "recommended_person": best_author,
        "reason": {
            "similar_issues_solved": best_count,
            "confidence": "high" if best_count >= 4 else "medium"
        },
        "other_possible_contacts": others
    }
