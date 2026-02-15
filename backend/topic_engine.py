import json
import os
import numpy as np
from collections import defaultdict

TOPIC_FILE = "data/topic_memory.json"
SIM_THRESHOLD = 0.72

# ---------- load / save ----------

def load_topics():
    if os.path.exists(TOPIC_FILE):
        with open(TOPIC_FILE, "r") as f:
            return json.load(f)
    return {"topics": []}

def save_topics(db):
    os.makedirs("data", exist_ok=True)
    with open(TOPIC_FILE, "w") as f:
        json.dump(db, f)

def cosine(a, b):
    return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-9))

# ---------- topic learning ----------

def learn_topic(vector, author, message):
    db = load_topics()

    best_id = None
    best_score = 0

    for topic in db["topics"]:
        score = cosine(vector, np.array(topic["centroid"]))
        if score > best_score:
            best_score = score
            best_id = topic["id"]

    # join existing topic
    if best_score > SIM_THRESHOLD:
        topic = next(t for t in db["topics"] if t["id"] == best_id)

        topic["centroid"] = (
            np.array(topic["centroid"]) * 0.9 + vector * 0.1
        ).tolist()

        topic["experts"][author] = topic["experts"].get(author,0) + 1

    # create new topic
    else:
        new_topic = {
            "id": len(db["topics"]),
            "centroid": vector.tolist(),
            "experts": {author:1}
        }
        db["topics"].append(new_topic)

    save_topics(db)

# ---------- expert search ----------

def find_experts(vector, top_k=3):
    db = load_topics()
    if not db["topics"]:
        return None

    best_topic = None
    best_score = 0

    for topic in db["topics"]:
        score = cosine(vector, np.array(topic["centroid"]))
        if score > best_score:
            best_score = score
            best_topic = topic

    if best_score < 0.55:
        return None

    ranked = sorted(
        best_topic["experts"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:top_k], best_score
