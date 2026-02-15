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
    try:
        experts = ask_brain(q)
        return experts
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health():
    return {"ok": True}
