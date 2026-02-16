print("🚀 MAIN FILE LOADED", flush=True)
from fastapi import FastAPI
from backend.github_webhook import router as github_router
from backend.search import ask_brain

import threading
import time
import json
import os

QUEUE_FILE = "data/commit_queue.json"

# lazy import (RAM safe)
def process_commit(commit):
    from backend.learner import learn_commit
    learn_commit(commit["author"], commit["message"])


def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r") as f:
            return json.load(f)
    return []

def save_queue(q):
    with open(QUEUE_FILE, "w") as f:
        json.dump(q, f, indent=2)


# ---------------- BACKGROUND WORKER ----------------
def background_worker():
    print("🧠 Background learner started", flush=True)

    while True:
        try:
            queue = load_queue()

            if queue:
                commit = queue.pop(0)
                save_queue(queue)

                print("Learning:", commit["author"], "|", commit["message"], flush=True)

                process_commit(commit)

            time.sleep(5)

        except Exception as e:
            print("Worker error:", e, flush=True)
            time.sleep(10)


# ---------------- FASTAPI ----------------
app = FastAPI()
app.include_router(github_router)


@app.on_event("startup")
def start_worker():
    print("Starting background worker...", flush=True)
    threading.Thread(target=background_worker, daemon=True).start()


@app.get("/")
def home():
    return {"status": "Company Brain Alive"}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/ask")
def ask(q: str):
    result = ask_brain(q)

    if result["status"] == "no_expert":
        return "No relevant expert found for this issue"

    expert = result["recommended_person"]
    count = result["reason"]["similar_issues_solved"]
    confidence = result["reason"]["confidence"]
    others = result["other_possible_contacts"]

    if count == 0:
        solved_text = "Has worked in this area but no direct fixes yet"
    elif count == 1:
        solved_text = "Solved 1 similar issue"
    else:
        solved_text = f"Solved {count} similar issues"

    others_text = ", ".join(others) if others else "No other expert found"

    formatted = f"""Recommended person: {expert}

Reason:
• {solved_text}
• Confidence level: {confidence}

Other possible contacts: {others_text}
"""

    return formatted
