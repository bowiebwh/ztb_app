
from fastapi import APIRouter
import requests, os

router = APIRouter()

@router.post("/infer")
def infer(prompt: str):
    r = requests.post(
        f"{os.getenv('OLLAMA_BASE')}/api/generate",
        json={"model": os.getenv("OLLAMA_MODEL"), "prompt": prompt}
    )
    return r.json()
