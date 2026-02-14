from fastapi import APIRouter, Request
from .learning import learn_issue

router = APIRouter()

@router.post("/github/webhook")
async def github_webhook(request: Request):

    payload = await request.json()

    employee = payload.get("pusher", {}).get("name", "Unknown")

    learned = []

    for commit in payload.get("commits", []):
        message = commit.get("message", "").strip()

        if not message:
            continue

        if message.lower().startswith("merge"):
            continue

        learn_issue(employee, message)
        learned.append(message)

    return {
        "status": "processed",
        "employee": employee,
        "learned_topics": learned
    }
