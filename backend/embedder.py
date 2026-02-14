import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}


def get_embedding(text: str):
    if not HF_TOKEN:
        raise Exception("HF_TOKEN not set in environment")

    response = requests.post(
        MODEL_URL,
        headers=headers,
        json={"inputs": text},
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(f"Embedding failed: {response.text}")

    return response.json()[0]
