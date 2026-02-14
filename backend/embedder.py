# embedder.py
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from huggingface_hub import login

# load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# login to huggingface (prevents rate limits & download failures)
if HF_TOKEN:
    login(token=HF_TOKEN)

# lightweight model (safe for free hosting)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model... (first time takes ~20s)")
model = SentenceTransformer(MODEL_NAME)
print("Model loaded successfully")

def get_embedding(text: str):
    if not text:
        return [0.0] * 384  # safe fallback
    return model.encode(text).tolist()
