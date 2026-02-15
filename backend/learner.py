from datetime import datetime
from backend.embedder import get_embedding
from backend.vectordb import add
from backend.expertise_db import update_expertise

def detect_topic(message: str):
    text = message.lower()

    auth_words = [
        "login","auth","token","jwt","session","signin","signup","password","credential"
    ]

    payment_words = [
        "payment","checkout","refund","transaction","upi","card","billing","invoice"
    ]

    db_words = [
        "db","database","query","sql","migration","schema","table","index"
    ]

    ui_words = [
        "ui","css","frontend","layout","button","responsive","design"
    ]

    def match(words):
        return any(w in text for w in words)

    if match(auth_words): return "authentication"
    if match(payment_words): return "payment"
    if match(db_words): return "database"
    if match(ui_words): return "frontend"

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
