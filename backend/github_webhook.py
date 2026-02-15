from fastapi import APIRouter, Request
from backend.learner import learn_commit

router = APIRouter()

@router.post("/webhook/github")
async def github_webhook(req: Request):
    try:
        payload = await req.json()
        commits = payload.get("commits", [])

        learned = 0

        for c in commits:
            try:
                author = c.get("author", {}).get("name", "unknown")
                message = c.get("message", "")

                if message.strip() == "":
                    continue

                learn_commit(author, message)
                learned += 1

            except Exception as e:
                print("Commit skipped:", e)

        return {"stored": learned}

    except Exception as e:
        print("Webhook failed:", e)
        return {"stored": 0}
