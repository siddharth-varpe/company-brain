from datetime import datetime
from .embedder import get_embedding
from .db.vector_store import add_memory

def learn_issue(employee: str, topic: str):

    embedding = get_embedding(topic)

    add_memory(employee, topic, embedding)

    return {
        "status": "learned",
        "employee": employee,
        "topic": topic
    }
