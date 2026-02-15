from fastapi import APIRouter, Request
from backend.learner import learn_commit

router = APIRouter()

@router.post("/webhook/github")
async def github_webhook(req: Request):
    payload = await req.json()

    commits = payload.get("commits", [])

    for c in commits:
        author = c.get("author", {}).get("name", "unknown")
        message = c.get("message", "")
        learn_commit(author, message)

    return {"stored": len(commits)}
