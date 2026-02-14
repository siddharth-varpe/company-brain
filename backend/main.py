from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from expert_finder import find_expert
from learning import learn_topic

app = FastAPI(title="Company Brain API")


# Health check (important for Render)
@app.get("/")
def root():
    return {"status": "alive", "service": "company-brain"}


# ---------------- LEARN ----------------
# Works in browser AND curl
@app.get("/learn")
@app.post("/learn")
def learn(employee: str = Query(...), topic: str = Query(...)):
    try:
        learn_topic(employee, topic)
        return {"status": "learned", "employee": employee, "topic": topic}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ---------------- ASK ----------------
# Works in browser AND curl
@app.get("/ask")
@app.post("/ask")
def ask(question: str = Query(...)):
    try:
        result = find_expert(question)
        return {"question": question, "answer": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
