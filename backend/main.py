from fastapi import FastAPI
from backend.github_webhook import router as github_router
from backend.search import ask_brain

app = FastAPI()

app.include_router(github_router)


@app.get("/")
def home():
    return {"status": "Company Brain Alive"}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/ask")
def ask(q: str):

    result = ask_brain(q)

    # ---------------- NO EXPERT ----------------
    if result["status"] == "no_expert":
        return "No relevant expert found for this issue yet."

    expert = result["recommended_person"]
    count = result["reason"]["similar_issues_solved"]
    confidence = result["reason"]["confidence"]
    others = result["other_possible_contacts"]

    # ---- fix zero count wording ----
    if count == 0:
        solved_text = "Has worked in this area but no exact similar issue recorded yet"
    elif count == 1:
        solved_text = "Solved 1 similar issue"
    else:
        solved_text = f"Solved {count} similar issues"

    # ---- fix others empty ----
    if not others:
        others_text = "No other expert found"
    else:
        others_text = ", ".join(others)

    formatted = f"""Recommended person: {expert}

Reason:
• {solved_text}
• Confidence level: {confidence}

Other possible contacts:
{others_text}
"""

    return formatted
