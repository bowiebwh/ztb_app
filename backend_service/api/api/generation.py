from datetime import datetime
import json
import logging
import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from minio_client import client, BUCKET
from text_parser import parse_file_bytes
from models import (
    GenerationTask,
    Project,
    FileRecord,
    DocumentContent,
    Material,
    MaterialBinding,
    DocumentChunk,
    TenderAnalysis as TenderAnalysisModel,
)
from schemas import GenerationTaskCreate, GenerationTaskRead
import sys, os
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
from .export import export_word
from .analysis import (
    _call_llm,
    extract_key_info_with_ollama,
    build_anythingllm_queries,
    _query_anythingllm,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def to_read_model(task: GenerationTask) -> GenerationTaskRead:
    return GenerationTaskRead(
        taskId=task.id,
        projectId=task.project_id,
        status=task.status,
        progress=task.progress,
        currentStage=task.current_stage,
        statusMessage=task.status_message,
        resultUrl=task.result_url,
        errorMessage=task.error_message,
        configId=task.config_id,
        startTime=task.started_at,
        updateTime=task.updated_at,
    )


def _build_section_prompt(
    project_name: str,
    summary: str,
    chapter: dict,
    kb_answer: str = "",
    key_info: dict | None = None,
    evidence: str = "",
) -> str:
    title = chapter.get("title") or chapter.get("heading") or "章节"
    sections = chapter.get("sections") or []
    # 使用编号列出要点，使输入更清晰
    sections_text = "\n".join([f"({i+1}) {s}" for i, s in enumerate(sections) if s])
    key_info_text = json.dumps(key_info or {}, ensure_ascii=False)
    
    return f"""你是一名专业的投标书撰写专家。你的任务是根据提供的所有资料，为项目「{project_name}」生成**当前章节**的正式投标书正文。

    [⚠️ 严格格式要求 - 必须遵守]
    1. **只输出本章节的**正文内容**，且必须保证内容在全文中是连续的。**
    2. **绝不能**包含任何开头称谓 (如“尊敬的...” “您好”等) 或结尾术语 (如“此致 敬礼” “顺祝商祺”等)。
    3. **绝不能**包含任何解释性文字、旁白或注释（如“请注意”、“注”、“本章节旨在说明”等）。
    4. 绝不能输出章节标题、编号、JSON、标签或任何Markdown格式。
    5. 确保在内容上与前后章节内容衔接自然，保持全文连贯的专业文风。
    6. 严禁输出“结语”“公司署名”“日期”等独立段落，严禁概括招标文件或新增未在章节要点内的主题。
    7. 必须完整展开“章节要点”中的每一项，使用正式表述串联成连续段落；不得生成空洞或与要点无关的内容。
    8. 如章节标题或要点包含编号/层级，需按原编号顺序组织表述，可在正文中使用对应的小标题编号，但不得新增未提供的小节。

    [项目信息]
    项目名称: {project_name}
    章节标题: {title}
    项目摘要 (仅供参考): {summary or "无"}

    [章节内容来源]
    章节要点 (须全部展开并整合):
    {sections_text or "无"}

    知识库要点 (可直接复用高质量表述):
    {kb_answer or "无"}

    招标关键信息 (JSON，仅作参考):
    {key_info_text}

    原文/证据 (可直接吸收的关键句子):
    {evidence or "无"}

    =======================================
    [写作要求 - 确保专业与连贯性]
    1. **语气与风格**: 必须采用**正式、严谨、专业的投标书**文体。内容应是以**我方**（三六零数字安全科技集团有限公司）的名义进行的方案陈述、能力展示或郑重承诺。
    2. **内容连贯**: 逐一、完整地吸收并**整合**“章节要点”中的所有内容，使用**流畅的过渡句和正式的措辞**将其融合成**连续、逻辑严密的段落或子章节**。
    3. **结构化细化**: 如果内容丰富，请在正文内部使用**二级或三级带编号的小标题**（例如：2.1.1、2.1.2 等）来组织内容，以增强文档的专业结构感。
    4. **占位符**: 必须保留并使用占位符（如 {{material:xxx}}）在正文中适当的位置，**不得改写、删除或解释占位符本身**。"""


def _generate_section_content(
    project_name: str,
    summary: str,
    chapter: dict,
    kb_answer: str = "",
    key_info: dict | None = None,
    evidence: str = "",
) -> str:
    prompt = _build_section_prompt(project_name, summary, chapter, kb_answer, key_info, evidence)
    resp = _call_llm(prompt)
    return str(resp).strip()


def _clean_markdown(text: str) -> str:
    """Strip simple Markdown markers (#, *, bullets) from text."""
    if not text:
        return text
    lines = []
    for line in str(text).splitlines():
        l = line.lstrip()
        if l.startswith("#"):
            l = l.lstrip("#").strip()
        l = re.sub(r"^[\-\*]\s*", "", l).strip()
        l = l.replace("**", "").replace("__", "")
        lines.append(l)
    return "\n".join(lines)


@router.post("/{project_id}", response_model=GenerationTaskRead)
def start_generation(
    project_id: int, payload: GenerationTaskCreate = None, db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    analysis = (
        db.query(TenderAnalysisModel)
        .filter(TenderAnalysisModel.project_id == project_id)
        .order_by(TenderAnalysisModel.updated_at.desc())
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=400, detail="请先完成招标内容解析后再生成投标书")

    summary = analysis.summary or ""
    raw_struct = json.loads(analysis.document_structure_json or "[]")

    if isinstance(raw_struct, dict):
        doc_struct = [raw_struct]
    elif isinstance(raw_struct, list):
        doc_struct = raw_struct
    else:
        doc_struct = []

    def normalize_sections(sections: any) -> list[str]:
        if not isinstance(sections, list):
            return [str(sections)] if sections is not None else []
        normalized: list[str] = []
        for s in sections:
            if isinstance(s, dict):
                normalized.append(str(s.get("content") or s.get("title") or s.get("text") or s))
            else:
                normalized.append(str(s))
        return normalized

    raw_text = _load_raw_text_for_project(db, project_id, max_chars=2000)
    key_info = extract_key_info_with_ollama(raw_text)
    queries = build_anythingllm_queries(key_info, project.name)
    kb_answers: list[str] = []
    for q in queries:
        try:
            ans = _query_anythingllm(q)
            if ans:
                kb_answers.append(f"【{q}】\n{ans}")
        except Exception as exc:
            logger.warning("anythingllm query failed | q=%s | %s", q, exc)
    kb_answer = "\n\n".join(kb_answers)

    def build_sections_with_generation(struct, summary_text: str) -> list[dict]:
        sections = []
        for ch in struct or []:
            if not isinstance(ch, dict):
                logger.warning("skip invalid chapter item: %s", ch)
                continue
            heading = ch.get("title") or ch.get("heading") or "章节"
            sec_list = normalize_sections(ch.get("sections") or [])
            evidence = raw_text[:500] if raw_text else ""
            try:
                body_text = _generate_section_content(
                    project.name,
                    summary_text,
                    {"title": heading, "sections": sec_list},
                    kb_answer=kb_answer,
                    key_info=key_info,
                    evidence=evidence,
                )
            except HTTPException:
                raise
            except Exception as exc:
                logger.exception("生成章节失败 | project_id=%s heading=%s", project_id, heading)
                raise HTTPException(status_code=502, detail=f"生成章节内容失败: {exc}")
            sections.append({"heading": heading, "level": 1, "body": body_text})
        if not sections and summary_text:
            sections.append({"heading": "概要", "level": 1, "body": summary_text})
        return sections

    generated_sections = build_sections_with_generation(doc_struct, summary)

    # 占位符素材替换：图片用特殊标记，文本类用解析出的正文
    bindings = (
        db.query(MaterialBinding)
        .filter(MaterialBinding.project_id == project_id)
        .all()
    )
    materials = {m.id: m for m in db.query(Material).all()}
    placeholder_map: dict[str, str] = {}
    for b in bindings:
        mat = materials.get(b.material_id)
        if not mat:
            continue
        if mat.type == "Image":
            replacement = f"[[IMAGE|{mat.url}|{mat.name}]]"
        else:
            text = _material_text(db, mat)
            replacement = text or (f"{mat.name}（{mat.url}）" if mat.url else mat.name)
        placeholder_map[str(b.placeholder_key)] = replacement

    def replace_placeholders(text: str) -> str:
        if not text or not placeholder_map:
            return text
        out = text
        for key, val in placeholder_map.items():
            out = out.replace(f"{{{{{key}}}}}", val)
            out = out.replace(f"{{{{ {key} }}}}", val)
            if ":" in key:
                short = key.split(":")[-1]
                out = out.replace(f"{{{{{short}}}}}", val)
                out = out.replace(f"{{{{ {short} }}}}", val)
        return out

    # 保留未替换占位符的正文用于前端编辑；生成替换版用于导出
    cleaned_sections: list[dict] = []
    replaced_sections: list[dict] = []
    for sec in generated_sections:
        heading_text = _clean_markdown(sec.get("heading") or sec.get("title") or "")
        body_text = _clean_markdown(str(sec.get("body") or ""))
        cleaned_sections.append({"heading": heading_text or "章节", "level": sec.get("level", 1), "body": body_text})
        replaced_sections.append(
            {
                "heading": replace_placeholders(heading_text or "章节"),
                "level": sec.get("level", 1),
                "body": replace_placeholders(body_text),
            }
        )

    full_content = "\n\n".join([f"{sec['heading']}\n{sec['body']}" for sec in replaced_sections])

    # 保存生成结果用于前端编辑展示，保留未替换的占位符
    doc_content = db.query(DocumentContent).filter(DocumentContent.project_id == project_id).first()
    try:
        existing = json.loads(doc_content.content_json) if doc_content and doc_content.content_json else {}
    except Exception:
        existing = {}
    if isinstance(existing, list):
        existing = {"content": existing, "structure": existing}

    new_payload = {
        "content": cleaned_sections,
        "structure": existing.get("structure") or doc_struct,
    }
    if not doc_content:
        doc_content = DocumentContent(project_id=project_id)
    doc_content.content_json = json.dumps(new_payload, ensure_ascii=False)
    db.add(doc_content)

    title = "投 标 文 件"
    filename = f"{project.name}.docx"
    # 封面信息
    bidder_name = "三六零数字安全科技集团有限公司"
    bid_date = (project.created_at or datetime.utcnow()).strftime("%Y年%m月%d日") if getattr(project, "created_at", None) else datetime.utcnow().strftime("%Y年%m月%d日")
    payload_export = {
        "title": title,
        "subtitle": "（正本）",
        "sections": replaced_sections,
        "content": full_content,
        "filename": filename,
        "project_name": project.name,
        "bidder_name": bidder_name,
        "bid_date": bid_date,
    }

    try:
        export_res = export_word(payload_export)
        logger.info(
            "Export word done for project %s | object=%s filename=%s",
            project_id,
            export_res.get("object_name"),
            export_res.get("filename"),
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Export word failed | project_id=%s", project_id)
        raise HTTPException(status_code=500, detail=f"生成投标书失败: {exc}")

    object_name = export_res.get("object_name")
    filename = export_res.get("filename") or f"{title}.docx"
    result_url = None

    # 记录生成文件到 FileRecord，便于前端下载
    if object_name:
        file_record = FileRecord(
            project_id=project_id,
            filename=filename,
            object_name=object_name,
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            size=export_res.get("size"),
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        result_url = f"/api/files/{file_record.id}/download"
        logger.info("Stored generated doc | project_id=%s file_id=%s object=%s url=%s", project_id, file_record.id, object_name, result_url)

    task = GenerationTask(
        project_id=project_id,
        status="Completed",
        progress=100.0,
        current_stage="Completed",
        status_message="生成完成",
        result_url=result_url,
        config_id=payload.config_id if payload else None,
        started_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    project.status = "Completed"

    project.updated_at = datetime.utcnow()
    db.add(task)
    db.add(project)
    db.commit()
    db.refresh(task)
    return to_read_model(task)


@router.post("/{project_id}/export_current", response_model=GenerationTaskRead)
def export_current(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    doc = db.query(DocumentContent).filter(DocumentContent.project_id == project_id).first()
    if not doc or not doc.content_json:
        raise HTTPException(status_code=400, detail="暂无可导出的文档内容，请先生成或编辑文档")

    try:
        parsed = json.loads(doc.content_json)
    except Exception:
        parsed = []
    if isinstance(parsed, dict):
        content_items = parsed.get("content") or []
    else:
        content_items = parsed or []

    def as_sections(items: list[dict]) -> list[dict]:
        out: list[dict] = []
        for item in items:
            title = item.get("heading") or item.get("title") or "章节"
            body = item.get("body") or ""
            out.append({"heading": title, "level": 1, "body": body})
        return out

    generated_sections = as_sections(content_items)

    # 占位符替换：图片用特殊标记，文本类用解析出的正文
    bindings = (
        db.query(MaterialBinding)
        .filter(MaterialBinding.project_id == project_id)
        .all()
    )
    materials = {m.id: m for m in db.query(Material).all()}
    placeholder_map: dict[str, str] = {}
    for b in bindings:
        mat = materials.get(b.material_id)
        if not mat:
            continue
        if mat.type == "Image":
            replacement = f"[[IMAGE|{mat.url}|{mat.name}]]"
        else:
            text = _material_text(db, mat)
            replacement = text or (f"{mat.name}（{mat.url}）" if mat.url else mat.name)
        placeholder_map[str(b.placeholder_key)] = replacement

    def replace_placeholders(text: str) -> str:
        if not text or not placeholder_map:
            return text
        out = text
        for key, val in placeholder_map.items():
            out = out.replace(f"{{{{{key}}}}}", val)
            out = out.replace(f"{{{{ {key} }}}}", val)
            if ":" in key:
                short = key.split(":")[-1]
                out = out.replace(f"{{{{{short}}}}}", val)
                out = out.replace(f"{{{{ {short} }}}}", val)
        return out

    for sec in generated_sections:
        sec["body"] = replace_placeholders(sec.get("body") or "")
        sec["heading"] = replace_placeholders(sec.get("heading") or "章节")

    full_content = "\n\n".join([f"{sec['heading']}\n{sec['body']}" for sec in generated_sections])

    title = "投 标 文 件"
    filename = f"{project.name}.docx"
    bidder_name = "三六零数字安全科技集团有限公司"
    bid_date = (project.created_at or datetime.utcnow()).strftime("%Y年%m月%d日") if getattr(project, "created_at", None) else datetime.utcnow().strftime("%Y年%m月%d日")
    payload_export = {
        "title": title,
        "subtitle": "（正本）",
        "sections": generated_sections,
        "content": full_content,
        "filename": filename,
        "project_name": project.name,
        "bidder_name": bidder_name,
        "bid_date": bid_date,
    }

    try:
        export_res = export_word(payload_export)
        logger.info(
            "Export current doc done for project %s | object=%s filename=%s",
            project_id,
            export_res.get("object_name"),
            export_res.get("filename"),
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Export current doc failed | project_id=%s", project_id)
        raise HTTPException(status_code=500, detail=f"导出失败: {exc}")

    object_name = export_res.get("object_name")
    filename = export_res.get("filename") or f"{title}.docx"
    result_url = None

    if object_name:
        file_record = FileRecord(
            project_id=project_id,
            filename=filename,
            object_name=object_name,
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            size=export_res.get("size"),
        )
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        result_url = f"/api/files/{file_record.id}/download"

    task = GenerationTask(
        project_id=project_id,
        status="Completed",
        progress=100.0,
        current_stage="Completed",
        status_message="导出完成",
        result_url=result_url,
        config_id=None,
        started_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    project.status = "Completed"
    project.updated_at = datetime.utcnow()
    db.add(task)
    db.add(project)
    db.commit()
    db.refresh(task)
    return to_read_model(task)
@router.get("/{project_id}/latest", response_model=GenerationTaskRead)
def get_latest_task(project_id: int, db: Session = Depends(get_db)):
    task = (
        db.query(GenerationTask)
        .filter(GenerationTask.project_id == project_id)
        .order_by(GenerationTask.updated_at.desc())
        .first()
    )
    if not task:
        now = datetime.utcnow()
        return GenerationTaskRead(
            taskId=0,
            projectId=project_id,
            status="Pending",
            progress=0.0,
            currentStage="Pending",
            statusMessage="等待生成",
            resultUrl=None,
            errorMessage=None,
            configId=None,
            startTime=now,
            updateTime=now,
        )
    return to_read_model(task)


@router.get("/{project_id}/history", response_model=list[GenerationTaskRead])
def get_history(project_id: int, db: Session = Depends(get_db)):
    tasks = (
        db.query(GenerationTask)
        .filter(GenerationTask.project_id == project_id)
        .order_by(GenerationTask.updated_at.desc())
        .all()
    )
    return [to_read_model(t) for t in tasks]


@router.get("/{project_id}/{task_id}", response_model=GenerationTaskRead)
def get_task(project_id: int, task_id: int, db: Session = Depends(get_db)):
    task = (
        db.query(GenerationTask)
        .filter(GenerationTask.project_id == project_id, GenerationTask.id == task_id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return to_read_model(task)


@router.post("/{project_id}/{task_id}/complete", response_model=GenerationTaskRead)
def complete_task(project_id: int, task_id: int, db: Session = Depends(get_db)):
    task = (
        db.query(GenerationTask)
        .filter(GenerationTask.project_id == project_id, GenerationTask.id == task_id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = "Completed"
    task.progress = 100.0
    task.current_stage = "Rendering"
    task.status_message = "生成完成"
    task.result_url = task.result_url or f"/api/files/download_case_study_word"
    task.updated_at = datetime.utcnow()

    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        project.status = "Completed"
        project.updated_at = datetime.utcnow()
        db.add(project)

    db.add(task)
    db.commit()
    db.refresh(task)
    return to_read_model(task)
def _material_text(db: Session, material: Material) -> str | None:
    """Load parsed text for a material from DocumentChunk, fallback to on-the-fly parse."""
    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.file_id == material.id)
        .order_by(DocumentChunk.chunk_index.asc())
        .all()
    )
    if not chunks:
        text_chunks = []
    else:
        text_chunks = [c.content or "" for c in chunks]
    text = "\n".join(text_chunks).strip() if text_chunks else ""
    if text:
        return text

    # Fallback: download from MinIO and parse
    def _extract_object_name(url: str | None) -> str | None:
        if not url:
            return None
        if "/download/" in url:
            return url.split("/download/", 1)[-1].lstrip("/")
        return url.lstrip("/")

    object_name = _extract_object_name(material.url)
    if not object_name:
        return None
    try:
        resp = client.get_object(BUCKET, object_name)
        data = resp.read()
        parsed = parse_file_bytes(material.name or object_name, data)
        text = "\n".join(parsed).strip()
        return text or None
    except Exception:
        logger.warning("Parse material text failed | material_id=%s object=%s", material.id, object_name)
    text = "\n".join([c.content or "" for c in chunks]).strip()
    return text or None


def _load_raw_text_for_project(db: Session, project_id: int, max_chars: int = 2000) -> str:
    files = (
        db.query(FileRecord)
        .filter(FileRecord.project_id == project_id)
        .order_by(FileRecord.created_at.desc())
        .all()
    )
    snippets: list[str] = []
    budget = max_chars
    for f in files:
        if budget <= 0:
            break
        lower = (f.filename or "").lower()
        if not lower.endswith((".pdf", ".doc", ".docx", ".txt", ".md")):
            continue
        try:
            obj = client.get_object(BUCKET, f.object_name)
            data = obj.read()
        finally:
            try:
                obj.close()
            except Exception:
                pass
        try:
            chunks = parse_file_bytes(f.filename, data)
        except Exception:
            continue
        raw = "\n".join(chunks)
        if not raw:
            continue
        trimmed = raw[:budget]
        snippets.append(f"[{f.filename}]\n{trimmed}")
        budget -= len(trimmed)
    return "\n\n".join(snippets)
