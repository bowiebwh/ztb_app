
from fastapi import APIRouter
import requests, os

router = APIRouter()

@router.post("/upload")
def upload_to_anythingllm(payload: dict):
    r = requests.post(
        f"{os.getenv('ANYTHINGLLM_BASE')}/api/documents/upload",
        headers={"Authorization": f"Bearer {os.getenv('ANYTHINGLLM_API_KEY')}"},
        json=payload
    )
    return r.json()
