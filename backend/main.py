from fastapi import FastAPI
from .expert_finder import find_expert
from .learning import learn_issue
from .github_webhook import router as github_router

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(github_router)


@app.get("/")
def home():
    return {"message": "Company Brain running"}


@app.get("/ask")
def ask_question(question: str):
    return find_expert(question)


@app.post("/learn")
def learn(employee: str, topic: str):
    return learn_issue(employee, topic)
