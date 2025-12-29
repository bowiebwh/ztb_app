
import io
import uuid
import os
import requests
from urllib.parse import quote
from fastapi import APIRouter, UploadFile, Depends, HTTPException, Response, Form
from sqlalchemy.orm import Session
from minio_client import client, BUCKET, ensure_bucket
from database import SessionLocal
from models import FileRecord, Project
from schemas import FileUploadResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload", response_model=FileUploadResponse)
def upload_file(
    project_id: int | None = Form(default=None),
    file: UploadFile = None,
    db: Session = Depends(get_db),
):
    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded")
    if project_id is None:
        raise HTTPException(status_code=400, detail="Missing project_id")

    project_exists = db.query(Project.id).filter(Project.id == project_id).first()
    if not project_exists:
        raise HTTPException(status_code=404, detail="Project not found")

    ensure_bucket()
    object_name = f"{uuid.uuid4()}_{file.filename}"
    data = io.BytesIO(file.file.read())
    size = data.getbuffer().nbytes
    data.seek(0)

    client.put_object(
        BUCKET,
        object_name,
        data,
        length=size,
        content_type=file.content_type or "application/octet-stream",
        part_size=10 * 1024 * 1024,
    )

    record = FileRecord(
        project_id=project_id,
        filename=file.filename,
        object_name=object_name,
        content_type=file.content_type,
        size=size,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    # Optional: ingest into AnythingLLM vector store
    anything_base = os.getenv("ANYTHINGLLM_BASE")
    api_key = os.getenv("ANYTHINGLLM_API_KEY")
    if anything_base and api_key:
        try:
            # Reset stream for upload
            data.seek(0)
            requests.post(
                f"{anything_base}/api/documents/upload",
                headers={"Authorization": f"Bearer {api_key}"},
                files={"file": (file.filename, data, file.content_type or "application/octet-stream")},
                timeout=30,
            )
        except Exception:
            # Ingestion failure should not block file upload; swallow/log silently.
            pass

    return FileUploadResponse(
        fileId=record.id,
        filename=record.filename,
        objectName=record.object_name,
        projectId=record.project_id,
        url=f"/api/files/{record.id}/download",
        contentType=record.content_type,
        size=record.size,
    )


@router.get("/{file_id}/download")
def download_file(file_id: int, db: Session = Depends(get_db)):
    record = db.query(FileRecord).filter(FileRecord.id == file_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        obj = client.get_object(BUCKET, record.object_name)
        data = obj.read()
    finally:
        try:
            obj.close()
        except Exception:
            pass

    filename = record.filename or "download"
    fallback = filename.encode("ascii", "ignore").decode() or "download"
    headers = {
        "Content-Disposition": f"attachment; filename=\"{fallback}\"; filename*=UTF-8''{quote(filename)}"
    }
    return Response(content=data, media_type=record.content_type or "application/octet-stream", headers=headers)


@router.get("/download/{object_name}")
def download_by_object(object_name: str):
    try:
        obj = client.get_object(BUCKET, object_name)
        data = obj.read()
    finally:
        try:
            obj.close()
        except Exception:
            pass
    filename = object_name.split("/")[-1] or "download"
    fallback = filename.encode("ascii", "ignore").decode() or "download"
    headers = {
        "Content-Disposition": f"attachment; filename=\"{fallback}\"; filename*=UTF-8''{quote(filename)}"
    }
    return Response(content=data, media_type="application/octet-stream", headers=headers)


@router.get("/", response_model=list[FileUploadResponse])
def list_files(project_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(FileRecord)
    if project_id is not None:
        query = query.filter(FileRecord.project_id == project_id)
    records = query.order_by(FileRecord.created_at.desc()).all()
    return [
        FileUploadResponse(
            fileId=r.id,
            filename=r.filename,
            objectName=r.object_name,
            projectId=r.project_id,
            url=f"/api/files/{r.id}/download",
            contentType=r.content_type,
            size=r.size,
        )
        for r in records
    ]


@router.get("/download_cert_pdf")
def download_cert_pdf():
    content = b"Dummy certificate PDF content"
    headers = {"Content-Disposition": 'attachment; filename="cert.pdf"'}
    return Response(content=content, media_type="application/pdf", headers=headers)


@router.get("/download_case_study_word")
def download_case_study_word():
    content = b"Dummy case study Word content"
    headers = {"Content-Disposition": 'attachment; filename="case-study.docx"'}
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers,
    )


@router.get("/download_price_excel")
def download_price_excel():
    content = b"Dummy price excel content"
    headers = {"Content-Disposition": 'attachment; filename="price.xlsx"'}
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )
