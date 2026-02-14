from backend.embedder import get_embedding
from backend.db.vector_store import add_memory, init_db

init_db()

def learn_topic(employee, topic):
    emb = get_embedding(topic)
    add_memory(employee, topic, emb)
