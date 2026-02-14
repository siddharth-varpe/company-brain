import os
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from huggingface_hub import login

# -------- FORCE LOAD .env FROM PROJECT ROOT --------
BASE_DIR = Path(__file__).resolve().parents[1]   # company-brain/
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise Exception(f"HF_TOKEN not found. Looked in: {ENV_PATH}")

# login once
login(token=HF_TOKEN)

# lightweight model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)
print("Model loaded successfully")

def get_embedding(text: str):
    if not text:
        return [0.0] * 384
    return model.encode(text).tolist()
