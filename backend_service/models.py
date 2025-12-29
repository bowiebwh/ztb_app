
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="Draft", nullable=False)
    current_step_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

class FileRecord(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=True)
    filename = Column(String(255), nullable=False)
    object_name = Column(String(255), nullable=False, unique=True)
    content_type = Column(String(128), nullable=True)
    size = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    url = Column(String(512), nullable=False)
    thumbnail_url = Column(String(512), nullable=True)
    icon_name = Column(String(100), nullable=True)
    upload_time = Column(DateTime(timezone=True), server_default=func.now())

class GenerationTask(Base):
    __tablename__ = "generation_tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    status = Column(String(50), default="InProgress", nullable=False)
    progress = Column(Float, default=0.0, nullable=False)
    current_stage = Column(String(100), nullable=True)
    status_message = Column(Text, nullable=True)
    result_url = Column(String(512), nullable=True)
    error_message = Column(Text, nullable=True)
    config_id = Column(String(100), nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

class TenderAnalysis(Base):
    __tablename__ = "tender_analysis"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    summary = Column(Text, nullable=True)
    key_dates_json = Column(Text, nullable=True)  # JSON string
    document_structure_json = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    file_id = Column(Integer, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PipelineTask(Base):
    __tablename__ = "pipeline_tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)  # ingest / chapter_generation / analysis
    status = Column(String(50), default="Pending", nullable=False)
    progress = Column(Float, default=0.0, nullable=False)
    result_json = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

class DocumentContent(Base):
    __tablename__ = "document_contents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False, unique=True)
    content_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

class MaterialBinding(Base):
    __tablename__ = "material_bindings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    placeholder_key = Column(String(255), nullable=False)
    material_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
