import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import PipelineTask, Project
from vector_store import search_chunks
from tasks import submit_task
import os
import requests

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _call_llm(prompt: str) -> str:
    base = os.getenv("OLLAMA_BASE")
    model = os.getenv("OLLAMA_MODEL", "qwen3:14B")
    if not base:
        raise Exception("OLLAMA_BASE not configured")
    resp = requests.post(
        f"{base}/api/generate",
        json={"model": model, "prompt": prompt},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("response") or json.dumps(data, ensure_ascii=False)


def _generate_chapters(project_id: int, outline: list):
    db = SessionLocal()
    try:
        results = []
        for chapter in outline:
            title = chapter.get("title", "未命名章节")
            query = chapter.get("query") or title
            hits = search_chunks(db, project_id, query, top_k=5)
            citations = "\n\n".join([f"[片段{i+1}] {c[1][:400]}" for i, c in enumerate(hits)])
            prompt = f"""你是投标书撰写专家，请撰写章节《{title}》，满足招标要求。可参考以下项目资料片段：
{citations or "无可用片段"}
请输出纯文本，不要包含多余的解释。"""
            content = _call_llm(prompt)
            results.append({"title": title, "content": content, "citations": hits})
        return results
    finally:
        db.close()


@router.post("/{project_id}")
def generate_chapters(project_id: int, payload: dict, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    outline = payload.get("outline") or []
    if not isinstance(outline, list) or not outline:
        raise HTTPException(status_code=400, detail="outline 不能为空")

    task = PipelineTask(project_id=project_id, type="chapter_generation", status="Pending", progress=0.0)
    db.add(task)
    db.commit()
    db.refresh(task)

    def runner():
        result = _generate_chapters(project_id, outline)
        db2 = SessionLocal()
        try:
            t = db2.query(PipelineTask).get(task.id)
            t.status = "Completed"
            t.progress = 100
            t.result_json = json.dumps(result, ensure_ascii=False)
            db2.add(t)
            db2.commit()
        finally:
            db2.close()
        return result

    submit_task(runner)
    return {"task_id": task.id, "status": "Pending"}
