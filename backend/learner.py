from datetime import datetime
from backend.embedder import get_embedding
from backend.topic_engine import learn_topic
from backend.vectordb import add


def learn_commit(author: str, message: str):

    # ignore empty commits
    if not message or not message.strip():
        return

    # create semantic embedding
    vector = get_embedding(message)

    # update knowledge brain
    learn_topic(vector, author, message)

    # store commit memory
    data = {
        "author": author,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }

    add(vector, data)
