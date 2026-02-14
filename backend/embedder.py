import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}


def get_embedding(text: str):

    if not text:
        return [0.0] * 384

    response = requests.post(API_URL, headers=headers, json={"inputs": text})

    if response.status_code != 200:
        return [0.0] * 384

    embedding = response.json()

    if isinstance(embedding[0], list):
        embedding = embedding[0]

    return embedding[:384]
