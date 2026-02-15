from collections import defaultdict
from backend.expertise_db import get_top_experts
from backend.embedder import get_embedding
from backend.vectordb import search


def ask_brain(question: str):

    # detect topic same way learner detects
    from backend.learner import detect_topic
    topic = detect_topic(question)

    # 1️⃣ Get experts by knowledge graph
    experts = get_top_experts(topic, k=3)

    if not experts:
        return {
            "status": "no_expert",
            "message": "No relevant expert found for this issue yet."
        }

    # 2️⃣ Validate using semantic evidence
    vec = get_embedding(question)
    evidence = search(vec)

    evidence_count = defaultdict(int)
    for r in evidence:
        evidence_count[r["author"]] += 1

    best = experts[0]
    similar_count = evidence_count.get(best, 0)

    return {
        "status": "expert_found",
        "recommended_person": best,
        "reason": {
            "topic": topic,
            "similar_issues_solved": similar_count,
            "confidence": "high" if similar_count >= 3 else "medium"
        },
        "other_possible_contacts": experts[1:]
    }
