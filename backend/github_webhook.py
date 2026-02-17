from fastapi import APIRouter, Request
import json
import os

router = APIRouter()

QUEUE_FILE = "data/commit_queue.json"


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
    print("📥 Webhook queued:", commit, flush=True)


@router.post("/webhook/github")
async def github_webhook(request: Request):
    payload = await request.json()

    if "commits" not in payload:
        return {"status": "ignored", "reason": "not a push event"}

    count = 0

    for c in payload["commits"]:
        message = c.get("message", "").strip()

        author = (
            c.get("author", {}).get("name")
            or payload.get("pusher", {}).get("name")
            or "unknown"
        )

        if not message:
            continue

        enqueue({
            "author": author,
            "message": message
        })

        count += 1

    return {"status": "processed", "count": count}
