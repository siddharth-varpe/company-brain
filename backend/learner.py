from backend.embedder import get_embedding
from backend.vectordb import add

def learn_commit(author: str, message: str):
    text = f"{author}: {message}"

    vector = get_embedding(text)

    data = {
        "author": author,
        "message": message
    }

    add(vector, data)
