from datetime import datetime, timedelta
from collections import defaultdict
from backend.embedder import get_embedding
from backend.vectordb import search


def recency_label(last_time):
    if not last_time:
        return "worked on this earlier"

    diff = datetime.utcnow() - last_time

    if diff < timedelta(days=1):
        return "worked on this today"
    elif diff < timedelta(days=7):
        return "worked on this recently"
    elif diff < timedelta(days=30):
        return "worked on this this month"
    else:
        return "worked on this earlier"


def ask_brain(question: str):
    vec = get_embedding(question)

    # fetch many matches to evaluate expertise
    results = search(vec, k=25)

    if not results:
        return "No expert learned yet."

    stats = defaultdict(lambda: {"count": 0, "last": None})

    # aggregate expertise
    for r in results:
        author = r.get("author", "unknown")
        stats[author]["count"] += 1

        ts = r.get("timestamp")
        if ts:
            try:
                t = datetime.fromisoformat(ts)
                if not stats[author]["last"] or t > stats[author]["last"]:
                    stats[author]["last"] = t
            except:
                pass

    # rank developers
    ranked = sorted(stats.items(), key=lambda x: x[1]["count"], reverse=True)

    best_author, best_data = ranked[0]
    others = [name for name, _ in ranked[1:3]]

    # ----- Build explanation -----
    lines = []
    lines.append(f"Recommended person: {best_author}")
    lines.append("")
    lines.append("Reason:")
    lines.append(f"• Solved {best_data['count']} similar issues")
    lines.append(f"• {recency_label(best_data['last'])}")

    if others:
        lines.append("")
        lines.append("Other possible contacts:")
        lines.append(", ".join(others))

    return "\n".join(lines)
