from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# lazy imports (CRITICAL)
@app.on_event("startup")
def load_routes():
    from .github_webhook import router as github_router
    from .learning import learn_issue
    from .expert_finder import find_expert

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
