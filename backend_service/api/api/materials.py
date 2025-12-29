import io
import os
import uuid

import requests
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from database import SessionLocal
from minio_client import BUCKET, client, ensure_bucket
from models import DocumentChunk
from models import Material as MaterialModel
from models import MaterialBinding
from schemas import Material, MaterialUploadResponse
from text_parser import parse_file_bytes

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[Material])
def list_materials(db: Session = Depends(get_db)):
    records = db.query(MaterialModel).order_by(MaterialModel.upload_time.desc()).all()
    return [
        Material(
            materialId=str(r.id),
            type=r.type,
            name=r.name,
            size=r.size,
            uploadTime=r.upload_time.isoformat() if r.upload_time else "",
            url=r.url,
            thumbnailUrl=r.thumbnail_url,
            iconName=r.icon_name,
        )
        for r in records
    ]


@router.post("/upload", response_model=MaterialUploadResponse)
def upload_material(file: UploadFile, db: Session = Depends(get_db)):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    ensure_bucket()
    object_name = f"materials/{uuid.uuid4()}_{file.filename}"
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

    mat = MaterialModel(
        type=_guess_material_type(file.filename, file.content_type),
        name=file.filename,
        size=size,
        url=f"/api/files/download/{object_name}",
        thumbnail_url=None,
        icon_name=_guess_icon(file.filename, file.content_type),
    )
    db.add(mat)
    db.commit()
    db.refresh(mat)

    # 文本类文件做 chunk 仅作本地 TF‑IDF 兜底，库内 project_id 固定 0
    if _is_textual(file.filename, file.content_type):
        data.seek(0)
        chunks = parse_file_bytes(file.filename, data.read())
        for idx, ch in enumerate(chunks):
            dc = DocumentChunk(
                project_id=0,
                file_id=mat.id,
                chunk_index=idx,
                content=ch,
            )
            db.add(dc)
        db.commit()

    # 推送 AnythingLLM（如已配置），让其负责切分+向量入库
    anything_base = os.getenv("ANYTHINGLLM_BASE")
    api_key = os.getenv("ANYTHINGLLM_API_KEY")
    if anything_base and api_key:
        try:
            data.seek(0)
            requests.post(
                f"{anything_base}/api/documents/upload",
                headers={"Authorization": f"Bearer {api_key}"},
                files={"file": (file.filename, data, file.content_type or "application/octet-stream")},
                timeout=60,
            )
        except Exception:
            # 不阻断主流程
            pass

    return MaterialUploadResponse(
        materialId=str(mat.id),
        type=mat.type,
        name=mat.name,
        size=mat.size,
        url=mat.url,
        contentType=file.content_type,
        iconName=mat.icon_name,
        uploadTime=mat.upload_time.isoformat() if mat.upload_time else "",
    )


def _guess_material_type(filename: str, content_type: str | None) -> str:
    lower = filename.lower()
    if lower.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
        return "Image"
    if lower.endswith(".pdf"):
        return "PDF"
    if lower.endswith((".doc", ".docx")):
        return "Word"
    if lower.endswith((".xls", ".xlsx")):
        return "Excel"
    if content_type and "image" in content_type:
        return "Image"
    return "Other"


def _guess_icon(filename: str, content_type: str | None) -> str:
    t = _guess_material_type(filename, content_type)
    return {
        "Image": "Image",
        "PDF": "FileText",
        "Word": "FileText",
        "Excel": "Table2",
    }.get(t, "File")


def _is_textual(filename: str, content_type: str | None) -> bool:
    lower = filename.lower()
    if lower.endswith((".pdf", ".doc", ".docx", ".txt", ".md")):
        return True
    if content_type and any(x in content_type for x in ["pdf", "word", "text"]):
        return True
    return False


@router.post("/bind")
def bind_material(payload: dict, db: Session = Depends(get_db)):
    project_id = payload.get("projectId")
    placeholder_key = payload.get("placeholderKey")
    material_id = payload.get("materialId")
    if not project_id or not placeholder_key or not material_id:
        raise HTTPException(status_code=400, detail="projectId/placeholderKey/materialId required")
    binding = MaterialBinding(
        project_id=project_id,
        placeholder_key=placeholder_key,
        material_id=material_id,
    )
    db.add(binding)
    db.commit()
    db.refresh(binding)
    return {"bindingId": binding.id}


@router.get("/bindings")
def list_bindings(project_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(MaterialBinding)
    if project_id is not None:
        query = query.filter(MaterialBinding.project_id == project_id)
    bindings = query.order_by(MaterialBinding.created_at.desc()).all()
    return [
        {
            "bindingId": b.id,
            "projectId": b.project_id,
            "placeholderKey": b.placeholder_key,
            "materialId": b.material_id,
        }
        for b in bindings
    ]


@router.delete("/bindings/{binding_id}")
def delete_binding(binding_id: int, db: Session = Depends(get_db)):
    binding = db.query(MaterialBinding).filter(MaterialBinding.id == binding_id).first()
    if not binding:
        raise HTTPException(status_code=404, detail="Binding not found")
    db.delete(binding)
    db.commit()
    return {"deleted": True, "bindingId": binding_id}
