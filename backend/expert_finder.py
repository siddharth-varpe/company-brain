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
    results = search_memory(question)

    if not results:
        return {
            "expert": "Unknown",
            "reason": "No knowledge learned yet",
            "evidence": []
        }

    best_employee, best_score, topics = results

    # Realistic threshold for MiniLM embeddings
    if best_score < 0.20:
        return {
            "expert": "Unknown",
            "reason": "Knowledge too unrelated",
            "evidence": []
        }

    return {
        "expert": best_employee,
        "reason": f"Similarity match ({confidence_label(best_score)})",
        "evidence": topics
    }
