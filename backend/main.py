from fastapi import FastAPI
from backend.github_webhook import router as github_router
from backend.search import ask_brain

app = FastAPI()

app.include_router(github_router)


@app.get("/")
def home():
    return {"status": "Company Brain Alive"}


@app.get("/ask")
def ask(q: str):
    return ask_brain(q)


@app.get("/health")
def health():
    return {"ok": True}

@app.get("/debug/db")
def debug_db():
    from backend.expertise_db import load_db
    db = load_db()
    return {
        "total_records": len(db),
        "sample": db[:5]
    }

@app.get("/admin/reset")
def reset():
    import os, json
    import faiss
    import numpy as np

    # recreate empty index
    dim = 384
    index = faiss.IndexFlatL2(dim)
    faiss.write_index(index, "data/index.faiss")

    # clear metadata
    with open("data/meta.json", "w") as f:
        json.dump([], f)

    return {"status": "brain reset"}
