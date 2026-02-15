from datetime import datetime
from backend.embedder import get_embedding
from backend.vectordb import add
from backend.expertise_db import update_expertise


def detect_topic(message: str):
    """
    Very simple topic detection (safe for now)
    Later we will upgrade to semantic clustering
    """
    text = message.lower()

    if "auth" in text or "login" in text or "token" in text or "jwt" in text:
        return "authentication"

    if "payment" in text or "checkout" in text or "transaction" in text:
        return "payment"

    if "db" in text or "database" in text or "query" in text:
        return "database"

    if "ui" in text or "css" in text or "frontend" in text:
        return "frontend"

    return "general"


def learn_commit(author: str, message: str):
    try:
        # 1️⃣ embedding
        vector = get_embedding(message)

        # 2️⃣ detect topic
        topic = detect_topic(message)

        # 3️⃣ update expertise index
        update_expertise(topic, author)

        # 4️⃣ store raw commit memory
        data = {
            "author": author,
            "message": message,
            "topic": topic,
            "timestamp": datetime.utcnow().isoformat()
        }

        add(vector, data)

    except Exception as e:
        print("Learning failed:", e)
