from backend.embedder import get_embedding
from backend.vectordb import add, search
from backend.expertise_db import update_expertise

def infer_topic(message, neighbors):
    """
    Topic = most common meaningful word among similar commits
    (simple but works surprisingly well)
    """
    words = message.lower().split()

    # remove noise words
    ignore = {"fix","fixed","added","update","updated","bug","issue","error","the","a","an","to","for"}
    words = [w for w in words if w not in ignore and len(w) > 3]

    if not words:
        return "general"

    return words[0]


def learn_commit(author: str, message: str):
    text = f"{author}: {message}"

    # 1️⃣ embed
    vec = get_embedding(text)

    # 2️⃣ find similar commits (topic detection)
    neighbors = search(vec, k=5)

    topic = infer_topic(message, neighbors)

    # 3️⃣ update expertise knowledge
    update_expertise(topic, author)

    # 4️⃣ store raw memory (training layer)
    data = {
        "author": author,
        "message": message,
        "topic": topic
    }

    add(vec, data)
