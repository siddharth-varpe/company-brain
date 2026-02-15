import json
import os
from datetime import datetime

FILE = "data/expertise.json"

if os.path.exists(FILE):
    with open(FILE, "r") as f:
        expertise = json.load(f)
else:
    expertise = {}


def save():
    with open(FILE, "w") as f:
        json.dump(expertise, f)


def decay_factor(last_time):
    last = datetime.fromisoformat(last_time)
    days = (datetime.utcnow() - last).days

    if days < 1: return 1.0
    if days < 7: return 0.8
    if days < 30: return 0.5
    if days < 90: return 0.2
    return 0.05


def update_expertise(topic, author):
    now = datetime.utcnow().isoformat()

    if topic not in expertise:
        expertise[topic] = {}

    if author not in expertise[topic]:
        expertise[topic][author] = {"score": 0, "last": now}

    # apply decay before updating
    factor = decay_factor(expertise[topic][author]["last"])
    expertise[topic][author]["score"] *= factor

    # add new knowledge
    expertise[topic][author]["score"] += 1
    expertise[topic][author]["last"] = now

    save()


def get_top_experts(topic, k=3):
    if topic not in expertise:
        return []

    ranked = sorted(
        expertise[topic].items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    return [name for name, _ in ranked[:k]]
