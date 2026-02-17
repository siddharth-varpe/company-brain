from fastapi import APIRouter, Request
import json
import os
from datetime import datetime

router = APIRouter()

QUEUE_FILE = "data/commit_queue.json"
os.makedirs("data", exist_ok=True)


def load_queue():
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r") as f:
            return json.load(f)
    return []


def save_queue(q):
    with open(QUEUE_FILE, "w") as f:
        json.dump(q, f, indent=2)


@router.post("/webhook/github")
async def github_webhook(request: Request):
    payload = await request.json()
    commits = payload.get("commits", [])

    queue = load_queue()

    added = 0
    for commit in commits:
        message = commit.get("message")
        author = commit.get("author", {}).get("name")

        if message and author:
            queue.append({
                "author": author,
                "message": message,
                "timestamp": datetime.utcnow().isoformat()
            })
            added += 1

    save_queue(queue)

    # IMPORTANT: instant success response for GitHub
    return {"status": "queued", "added": added}
