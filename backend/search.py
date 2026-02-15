from backend.embedder import get_embedding
from backend.topic_engine import find_experts


def ask_brain(question: str):

    if not question.strip():
        return {
            "status": "no_expert",
            "message": "Empty question"
        }

    vector = get_embedding(question)

    result = find_experts(vector)

    if not result:
        return {
            "status": "no_expert",
            "message": "No relevant expert found for this issue yet."
        }

    ranked, confidence_score = result

    best_author = ranked[0][0]
    best_count = ranked[0][1]

    others = [name for name,_ in ranked[1:]]

    confidence = "high" if confidence_score > 0.75 else "medium"

    return {
        "status": "expert_found",
        "recommended_person": best_author,
        "reason": {
            "similar_issues_solved": best_count,
            "confidence": confidence
        },
        "other_possible_contacts": others
    }
