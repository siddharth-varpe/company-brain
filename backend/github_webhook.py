from fastapi import APIRouter, Request
from backend.learner import learn_commit

router = APIRouter()


@router.post("/webhook/github")
async def github_webhook(req: Request):
    payload = await req.json()

    # GitHub sends many events — we only care about push commits
    commits = payload.get("commits", [])

    stored = 0

    for c in commits:
        # -------------------------------
        # REAL AUTHOR IDENTITY (important)
        # -------------------------------
        author = (
            c.get("author", {}).get("username")  # GitHub username (best)
            or c.get("author", {}).get("name")   # fallback to git name
            or "unknown"
        )

        message = c.get("message", "").strip()

        # ignore empty commits
        if not message:
            continue

        learn_commit(author, message)
        stored += 1

    return {"stored": stored}
