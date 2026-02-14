from .embedder import get_embedding
from .db.vector_store import search_memory


def confidence_label(score: float):
    if score > 0.75:
        return "High confidence"
    elif score > 0.45:
        return "Medium confidence"
    elif score > 0.25:
        return "Low confidence"
    return "Very weak"


def find_expert(question: str):
    # 1️⃣ Convert question → embedding
    question_embedding = get_embedding(question)

    # 2️⃣ Search vector database
    result = search_memory(question_embedding)

    if not result:
        return {
            "expert": "Unknown",
            "reason": "No matching knowledge found",
            "evidence": []
        }

    employee, score, topics = result

    # very low threshold because semantic similarity is subtle
    if score < 0.15:
        return {
            "expert": "Unknown",
            "reason": "Issue unrelated to known work",
            "evidence": []
        }

    return {
        "expert": employee,
        "reason": f"Matched past work ({confidence_label(score)})",
        "evidence": topics
    }
