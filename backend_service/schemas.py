from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# ---------- Project ----------

class ProjectCreate(BaseModel):
    project_name: str = Field(..., alias="projectName")
    description: Optional[str] = None
    current_step_id: Optional[str] = Field(None, alias="currentStepId")

    class Config:
        allow_population_by_field_name = True


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = Field(None, alias="projectName")
    description: Optional[str] = None
    status: Optional[str] = None
    current_step_id: Optional[str] = Field(None, alias="currentStepId")

    class Config:
        allow_population_by_field_name = True


class ProjectRead(BaseModel):
    project_id: str = Field(..., alias="projectId")
    project_name: str = Field(..., alias="projectName")
    status: str
    create_time: datetime = Field(..., alias="createTime")
    update_time: datetime = Field(..., alias="updateTime")
    current_step_id: Optional[str] = Field(None, alias="currentStepId")
    description: Optional[str] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# ---------- Files / Materials ----------

class FileUploadResponse(BaseModel):
    file_id: int = Field(..., alias="fileId")
    filename: str
    object_name: str = Field(..., alias="objectName")
    project_id: Optional[int] = Field(None, alias="projectId")
    url: str
    content_type: Optional[str] = Field(None, alias="contentType")
    size: Optional[int]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Material(BaseModel):
    material_id: str = Field(..., alias="materialId")
    type: str
    name: str
    size: int
    upload_time: str = Field(..., alias="uploadTime")
    url: str
    thumbnail_url: Optional[str] = Field(None, alias="thumbnailUrl")
    icon_name: Optional[str] = Field(None, alias="iconName")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class MaterialUploadResponse(BaseModel):
    material_id: str = Field(..., alias="materialId")
    type: str
    name: str
    size: int
    url: str
    content_type: Optional[str] = Field(None, alias="contentType")
    thumbnail_url: Optional[str] = Field(None, alias="thumbnailUrl")
    icon_name: Optional[str] = Field(None, alias="iconName")
    upload_time: str = Field(..., alias="uploadTime")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class MaterialPage(BaseModel):
    items: List[Material]
    total: int
    page: int
    page_size: int = Field(..., alias="pageSize")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# ---------- Tender Analysis ----------

class TenderAnalysis(BaseModel):
    summary: str
    key_dates: List[dict] = Field(..., alias="keyDates")
    document_structure: List[dict] = Field(..., alias="documentStructure")

    class Config:
        allow_population_by_field_name = True


# ---------- Generation ----------

class GenerationTaskCreate(BaseModel):
    config_id: Optional[str] = Field(None, alias="configId")

    class Config:
        allow_population_by_field_name = True


class GenerationTaskRead(BaseModel):
    task_id: int = Field(..., alias="taskId")
    project_id: int = Field(..., alias="projectId")
    status: str
    progress: float
    current_stage: Optional[str] = Field(None, alias="currentStage")
    status_message: Optional[str] = Field(None, alias="statusMessage")
    result_url: Optional[str] = Field(None, alias="resultUrl")
    error_message: Optional[str] = Field(None, alias="errorMessage")
    config_id: Optional[str] = Field(None, alias="configId")
    start_time: datetime = Field(..., alias="startTime")
    update_time: datetime = Field(..., alias="updateTime")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
