import json
import time
from backend.learner import learn_commit

QUEUE_FILE = "data/pending_commits.json"


def load_queue():
    try:
        with open(QUEUE_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_queue(queue):
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)


def worker_loop():
    print("🧠 Background learner started")

    while True:
        queue = load_queue()
        changed = False

        for item in queue:
            if not item.get("processed"):
                print("Processing:", item["message"])

                learn_commit(item["author"], item["message"])

                item["processed"] = True
                changed = True

        if changed:
            save_queue(queue)

        time.sleep(5)  # check every 5 sec
