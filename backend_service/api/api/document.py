import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import TenderAnalysis, Project, GenerationTask, DocumentContent

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{project_id}")
def get_document(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    analysis = (
        db.query(TenderAnalysis)
        .filter(TenderAnalysis.project_id == project_id)
        .order_by(TenderAnalysis.updated_at.desc())
        .first()
    )
    latest_task = (
        db.query(GenerationTask)
        .filter(GenerationTask.project_id == project_id)
        .order_by(GenerationTask.updated_at.desc())
        .first()
    )
    return {
        "projectId": project.id,
        "projectName": project.name,
        "analysis": {
            "summary": analysis.summary if analysis else "",
            "documentStructure": json.loads(analysis.document_structure_json or "[]") if analysis else [],
            "keyDates": json.loads(analysis.key_dates_json or "[]") if analysis else [],
        },
        "latestTask": {
            "taskId": latest_task.id if latest_task else None,
            "status": latest_task.status if latest_task else None,
            "resultUrl": latest_task.result_url if latest_task else None,
        },
    }


@router.get("/{project_id}/structure")
def get_structure(project_id: int, db: Session = Depends(get_db)):
    doc = db.query(DocumentContent).filter(DocumentContent.project_id == project_id).first()
    if not doc:
        return {"projectId": project_id, "content": [], "structure": []}
    try:
        parsed = json.loads(doc.content_json or "[]")
    except Exception:
        parsed = []

    # 兼容旧数据：纯数组表示正文，同时作为结构返回
    if isinstance(parsed, list):
        content = parsed
        structure = parsed
    elif isinstance(parsed, dict):
        content = parsed.get("content") or []
        structure = parsed.get("structure") or []
        # 兼容仅有 content 或 structure 的情况
        if not content and isinstance(parsed.get("structure"), list):
            content = parsed.get("structure")
        if not structure and isinstance(parsed.get("content"), list):
            structure = parsed.get("content")
    else:
        content = []
        structure = []

    return {"projectId": project_id, "content": content, "structure": structure}


@router.post("/{project_id}/structure")
def save_structure(project_id: int, payload: dict, db: Session = Depends(get_db)):
    content = payload.get("content", [])
    structure = payload.get("structure")
    doc = db.query(DocumentContent).filter(DocumentContent.project_id == project_id).first()
    try:
        existing = json.loads(doc.content_json) if doc and doc.content_json else {}
    except Exception:
        existing = {}
    if isinstance(existing, list):
        existing = {"content": existing, "structure": existing}
    new_data = {
        "content": content,
        "structure": structure if structure is not None else existing.get("structure", []),
    }
    doc = db.query(DocumentContent).filter(DocumentContent.project_id == project_id).first()
    if not doc:
        doc = DocumentContent(project_id=project_id, content_json=json.dumps(new_data, ensure_ascii=False))
    else:
        doc.content_json = json.dumps(new_data, ensure_ascii=False)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"projectId": project_id, "content": new_data.get("content"), "structure": new_data.get("structure")}
