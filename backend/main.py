from fastapi import FastAPI
from backend.github_webhook import router as github_router
from backend.search import ask_brain

import threading
import time
import json
import os

print("🚀 MAIN FILE LOADED", flush=True)

app = FastAPI()

# attach routes AFTER app creation
app.include_router(github_router)

QUEUE_FILE = "data/commit_queue.json"


# ---------------- QUEUE STORAGE ----------------

def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r") as f:
            return json.load(f)
    return []


def save_queue(q):
    with open(QUEUE_FILE, "w") as f:
        json.dump(q, f, indent=2)


def enqueue(commit):
    q = load_queue()
    q.append(commit)
    save_queue(q)
    print("📥 Commit queued:", commit, flush=True)


def dequeue():
    q = load_queue()
    if not q:
        return None
    commit = q.pop(0)
    save_queue(q)
    return commit


# ---------------- PROCESSOR ----------------

def process_commit(commit):
    from backend.learner import learn_commit
    print("🧠 Processing:", commit, flush=True)
    learn_commit(commit["author"], commit["message"])


def background_worker():
    print("🧵 Background learner started", flush=True)
    while True:
        commit = dequeue()
        if commit:
            process_commit(commit)
        time.sleep(2)


# start worker
threading.Thread(target=background_worker, daemon=True).start()


# ---------------- API ----------------

@app.get("/")
def home():
    return {"status": "brain running"}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/ask")
def ask(question: str):
    return ask_brain(question)
