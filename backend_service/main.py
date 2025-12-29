
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import (
    projects,
    files,
    llm,
    anythingllm,
    generation,
    analysis,
    materials,
    export,
    pipeline,
    chapters,
    document,
)
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="UXBot Enterprise Backend")

# CORS: allow frontend dev host
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(files.router, prefix="/api/files", tags=["Files"])
app.include_router(anythingllm.router, prefix="/api/anythingllm", tags=["AnythingLLM"])
app.include_router(llm.router, prefix="/api/llm", tags=["LLM"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["TenderAnalysis"])
app.include_router(
    generation.router, prefix="/api/generation", tags=["GenerationTasks"]
)
app.include_router(materials.router, prefix="/api/materials", tags=["Materials"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])
app.include_router(pipeline.router, prefix="/api/pipeline", tags=["Pipeline"])
app.include_router(chapters.router, prefix="/api/chapters", tags=["Chapters"])
app.include_router(document.router, prefix="/api/document", tags=["Document"])
