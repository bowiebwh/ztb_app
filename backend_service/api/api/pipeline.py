import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import PipelineTask, Project, FileRecord, DocumentChunk
from minio_client import client, BUCKET
from text_parser import parse_file_bytes
from tasks import submit_task

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _ingest_project(project_id: int):
    db = SessionLocal()
    try:
        files = db.query(FileRecord).filter(FileRecord.project_id == project_id).all()
        if not files:
            raise Exception("no files to ingest")
        chunk_count = 0
        for f in files:
            obj = client.get_object(BUCKET, f.object_name)
            data = obj.read()
            chunks = parse_file_bytes(f.filename, data)
            for idx, ch in enumerate(chunks):
                dc = DocumentChunk(
                    project_id=project_id,
                    file_id=f.id,
                    chunk_index=idx,
                    content=ch,
                )
                db.add(dc)
                chunk_count += 1
        db.commit()
        return {"chunks": chunk_count}
    finally:
        db.close()


@router.post("/ingest/{project_id}")
def ingest(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    task = PipelineTask(project_id=project_id, type="ingest", status="Pending", progress=0.0)
    db.add(task)
    db.commit()
    db.refresh(task)

    def runner():
        result = _ingest_project(project_id)
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


@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(PipelineTask).filter(PipelineTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "taskId": task.id,
        "type": task.type,
        "status": task.status,
        "progress": task.progress,
        "result": json.loads(task.result_json or "{}"),
        "errorMessage": task.error_message,
        "updatedAt": task.updated_at,
    }
