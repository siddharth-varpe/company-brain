from fastapi import FastAPI, Query
from learning import learn_topic
from expert_finder import find_expert

app = FastAPI()


@app.get("/")
def health():
    return {"status": "running"}


@app.get("/learn")
def learn(employee: str, topic: str):
    learn_topic(employee, topic)
    return {"message": "learned", "employee": employee, "topic": topic}


@app.get("/ask")
def ask(question: str):
    answer = find_expert(question)
    return {"answer": answer}
