import math
from datetime import datetime, timedelta
from sklearn.metrics.pairwise import cosine_similarity

from .embedder import get_embedding
from .db.vector_store import search_memory


# ---------------- CONFIDENCE LABEL ----------------

def confidence_label(score: float) -> str:
    if score > 0.75:
        return "Very High confidence"
    elif score > 0.55:
        return "High confidence"
    elif score > 0.35:
        return "Medium confidence"
    elif score > 0.20:
        return "Low confidence"
    else:
        return "Very Low confidence"


# ------------- SUPPORTING EVIDENCE ----------------

def get_supporting_topics(memories, employee, limit=3):
    related = []
    for m in memories:
        if m["employee"] == employee:
            related.append(m["topic"])
    return related[:limit]


# ---------------- MAIN LOGIC ----------------------

def find_expert(question: str):

    # Convert question to embedding
    query_vector = get_embedding(question)

    # Retrieve similar past memories
    memories = search_memory(query_vector, k=20)

    if not memories:
        return {
            "expert": "Unknown",
            "reason": "No similar knowledge found in company memory",
            "evidence": []
        }

    recent_scores = {}
    historical_scores = {}

    # Evaluate memories
    for record in memories:

        employee = record["employee"]
        timestamp = datetime.fromisoformat(record["timestamp"])

        # Recompute similarity
        topic_embedding = get_embedding(record["topic"])
        similarity = cosine_similarity([query_vector], [topic_embedding])[0][0]

        if math.isnan(similarity) or similarity < 0.25:
            continue

        # Priority: recent work first (last 3 days)
        if datetime.now() - timestamp < timedelta(days=3):
            recent_scores[employee] = recent_scores.get(employee, 0) + similarity
        else:
            historical_scores[employee] = historical_scores.get(employee, 0) + similarity

    # ---------------- DECISION ----------------

    # Priority 1: recent expert
    if recent_scores:
        best_employee = max(recent_scores, key=recent_scores.get)
        best_score = recent_scores[best_employee]
        topics = get_supporting_topics(memories, best_employee)

        return {
            "expert": best_employee,
            "reason": f"Recently worked on similar issue ({confidence_label(best_score)})",
            "evidence": topics
        }

    # Priority 2: historical expert
    if historical_scores:
        best_employee = max(historical_scores, key=historical_scores.get)
        best_score = historical_scores[best_employee]
        topics = get_supporting_topics(memories, best_employee)

        return {
            "expert": best_employee,
            "reason": f"Worked on similar issues before ({confidence_label(best_score)})",
            "evidence": topics
        }

    # Priority 3: unknown
    return {
        "expert": "Unknown",
        "reason": "No confident match found",
        "evidence": []
    }
