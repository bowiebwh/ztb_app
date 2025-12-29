
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Project
from schemas import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def project_to_read_model(p: Project) -> ProjectRead:
    return ProjectRead(
        projectId=str(p.id),
        projectName=p.name,
        status=p.status,
        createTime=p.created_at,
        updateTime=p.updated_at,
        currentStepId=p.current_step_id,
        description=p.description,
    )


@router.post("/", response_model=ProjectRead)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(
        name=payload.project_name,
        description=payload.description,
        current_step_id=payload.current_step_id or "upload_tender_document_step",
        status="Draft",
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project_to_read_model(project)


@router.get("/", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return [project_to_read_model(p) for p in projects]


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_to_read_model(project)


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if payload.project_name is not None:
        project.name = payload.project_name
    if payload.description is not None:
        project.description = payload.description
    if payload.status is not None:
        project.status = payload.status
    if payload.current_step_id is not None:
        project.current_step_id = payload.current_step_id
    project.updated_at = datetime.utcnow()

    db.add(project)
    db.commit()
    db.refresh(project)
    return project_to_read_model(project)


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"success": True}
