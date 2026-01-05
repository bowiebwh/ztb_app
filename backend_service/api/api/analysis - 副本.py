import json
import os
import re
import logging
from typing import Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import SessionLocal
from minio_client import BUCKET, client
from models import FileRecord, Project
from models import TenderAnalysis as TenderAnalysisModel, DocumentContent
from schemas import TenderAnalysis
from text_parser import parse_file_bytes
from vector_store import search_chunks

logger = logging.getLogger(__name__)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _query_anythingllm(question: str) -> Optional[str]:
    base = os.getenv("ANYTHINGLLM_BASE")
    api_key = os.getenv("ANYTHINGLLM_API_KEY")
    if not base or not api_key:
        return None
    try:
        resp = requests.post(
            f"{base}/api/query",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"query": question},
            timeout=45,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("answer") or json.dumps(data)
    except Exception:
        return None


def _call_llm(prompt: str) -> str:
    base = os.getenv("OLLAMA_BASE")
    model = os.getenv("OLLAMA_MODEL", "qwen3:14B")
    timeout = int(os.getenv("OLLAMA_TIMEOUT", "300"))
    if not base:
        raise HTTPException(status_code=500, detail="OLLAMA_BASE not configured")
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            # 关闭流式，避免多行 JSON 难以解析
            "stream": False,
        }
        resp = requests.post(f"{base}/api/generate", json=payload, timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="LLM请求超时，请检查模型是否已加载或调大 OLLAMA_TIMEOUT")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM 请求失败: {exc}")
    # 优先解析 JSON；若失败尝试逐行 JSON 解析；最后返回原始文本
    try:
        data = resp.json()
    except Exception:
        lines = [l for l in resp.text.splitlines() if l.strip()]
        data = None
        for line in lines:
            try:
                data = json.loads(line)
                break
            except Exception:
                continue
        if not data:
            logger.warning("LLM 原始文本预览（非 JSON）: %s", (resp.text or "")[:400])
            return resp.text
    return data.get("response") or data.get("message") or json.dumps(data)


def _is_textual(filename: str, content_type: str | None) -> bool:
    lower = filename.lower()
    if lower.endswith((".pdf", ".doc", ".docx", ".txt", ".md")):
        return True
    if content_type and any(x in content_type for x in ["pdf", "word", "text"]):
        return True
    return False


def _read_raw_text(files: list[FileRecord], max_chars: int = 2000) -> str:
    """
    直接从 MinIO 读取原文做推理上下文，不做本地 chunk/embedding 持久化。
    """
    snippets: list[str] = []
    budget = max_chars
    for f in files:
        if budget <= 0:
            break
        if not _is_textual(f.filename, f.content_type):
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


def _parse_llm_json(raw: str | dict) -> dict:
    """
    尽可能宽容地从 LLM 响应中提取首个 JSON 对象。
    - 直接是 dict: 原样返回
    - 代码块/多余文本: 去除围栏，使用 JSONDecoder 从首个 { 开始 raw_decode
    """
    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        raise ValueError("LLM 返回类型非字符串/字典")

    text = raw.strip()
    # 去掉 ```json/``` 包裹
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"```$", "", text).strip()

    decoder = json.JSONDecoder()
    # 找到首个 {
    brace = re.search(r"\{", text)
    if brace:
        try:
            obj, _ = decoder.raw_decode(text[brace.start():])
            return obj
        except Exception:
            pass

    # 回退直接 loads（可能全量就是 JSON）
    return json.loads(text)

DEFAULT_SUMMARY_PLACEHOLDER = "暂无模型总结，请检查招标文件与模型输出。"


def _analyze_core(project_id: int, db: Session, refresh: bool = False) -> TenderAnalysis:
    """
    Flow:
    - fetch project; 404 if missing
    - fetch project files; 400 if none (ask for upload)
    - return cached result when valid, no new files, and refresh=False
    - otherwise call LLM to regenerate and sync DocumentContent
    """
    project: Project | None = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    record = (
        db.query(TenderAnalysisModel)
        .filter(TenderAnalysisModel.project_id == project_id)
        .order_by(TenderAnalysisModel.updated_at.desc())
        .first()
    )

    files = (
        db.query(FileRecord)
        .filter(FileRecord.project_id == project_id)
        .order_by(FileRecord.created_at.desc())
        .all()
    )
    if not files:
        logger.warning(
            "no tender files when analyzing | project_id=%s cached=%s files_in_db=0",
            project_id,
            bool(record),
        )
        raise HTTPException(status_code=400, detail="未找到招标文件，请先上传后再分析")

    latest_file_time = files[0].created_at
    summary_cached = ""
    key_dates_cached: list[dict] = []
    doc_struct_cached: list[dict] = []
    has_new_file = False

    if record:
        summary_cached = record.summary or ""
        key_dates_cached = json.loads(record.key_dates_json or "[]")
        doc_struct_cached = json.loads(record.document_structure_json or "[]")
        has_new_file = bool(latest_file_time and record.updated_at and record.updated_at < latest_file_time)
        is_placeholder = summary_cached.strip() == DEFAULT_SUMMARY_PLACEHOLDER
        is_cached_valid = (
            bool(summary_cached.strip())
            and not is_placeholder
            and len(key_dates_cached) > 0
            and len(doc_struct_cached) > 0
        )
        if not refresh and is_cached_valid and not has_new_file:
            logger.info(
                "analysis cache hit | project_id=%s updated_at=%s latest_file=%s",
                project_id,
                record.updated_at,
                latest_file_time,
            )
            return TenderAnalysis(
                summary=summary_cached,
                keyDates=key_dates_cached,
                documentStructure=doc_struct_cached,
            )

    file_list_text = "\n".join([f"- {f.filename}" for f in files]) or "(no files)"

    raw_text = _read_raw_text(files)

    # === NEW: extract key info with Ollama ===
    key_info = extract_key_info_with_ollama(raw_text)
    logger.info("extracted tender key info: %s", key_info)

    # === NEW: targeted AnythingLLM queries ===
    queries = build_anythingllm_queries(key_info, project.name)

    kb_answers: list[str] = []
    for q in queries:
        try:
            ans = _query_anythingllm(q)
            if ans:
                kb_answers.append(f"【{q}】\n{ans}")
        except Exception as exc:
            logger.warning("anythingllm query failed | q=%s | %s", q, exc)

    kb_answer = "\n\n".join(kb_answers) or "knowledge base empty"

    # local TF-IDF snippets for quick grounding
    chunk_hits = search_chunks(db, project_id, project.name, top_k=5)
    citations_text = "\n".join([f"[chunk{i+1}] {c[1][:200]}" for i, c in enumerate(chunk_hits)])

    prompt = f"""你是招投标技术方案分析专家，请输出结构化 JSON，内容充分、中文输出。
    <知识库要点>
    {kb_answer}
    </知识库要点>
    <项目文件列表>
    {file_list_text}
    </项目文件列表>
    <原文摘录>
    {raw_text or "无原文摘录"}
    </原文摘录>
    <本地TFIDF片段>
    {citations_text or "无"}
    </本地TFIDF片段>

    占位符要求：
    - 在 documentStructure.sections 中加入占位符（示例：{{material:company_intro}}、{{material:case_study}}、{{material:qualification}}），便于后续材料库替换。
    - 占位符需有意义且保持中文描述，即使内容简短也不要移除。

    输出 JSON 字段：
    - summary：至少 3 条完整句子，概括需求/风险
    - keyDates：至少 3 条，每条含 label/date
    - documentStructure：不少于 5 个章节，含 id/title/sections[]，章节描述非空、条目丰富
    """
    logger.info("LLM 提示词 (project %s):\n%s", project_id, prompt[:2000])
    llm_resp: str | dict | None = None
    try:
        llm_resp = _call_llm(prompt)
        logger.warning("LLM 原始响应预览: %s", (str(llm_resp)[:400] if llm_resp is not None else "<no-response>"))
        parsed = _parse_llm_json(llm_resp)
    except HTTPException:
        raise
    except Exception as exc:
        raw_preview = str(llm_resp) if llm_resp is not None else "<no-response>"
        if len(raw_preview) > 800:
            raw_preview = raw_preview[:800] + "...(truncated)"
        logger.warning("LLM response parse failed: %s | raw=%s", exc, raw_preview)
        # 解析失败时使用默认占位，不中断流程，保证前端仍可获得结果
        parsed = {}

    summary = parsed.get("summary", "")
    if isinstance(summary, list):
        summary = " ".join([str(s) for s in summary])
    if isinstance(summary, dict):
        summary = " ".join([f"{k}:{v}" for k, v in summary.items()])
    summary = str(summary) if summary is not None else ""
    summary = summary or "暂无模型总结，请检查招标文件与模型输出。"

    # keyDates 兼容 value/date 字段
    key_dates_raw = parsed.get("keyDates", [])
    key_dates: list[dict] = []
    if isinstance(key_dates_raw, list):
        for item in key_dates_raw:
            if isinstance(item, dict):
                label = item.get("label") or item.get("name") or item.get("title") or "关键时间"
                date_val = item.get("date") or item.get("value") or item.get("time") or ""
                key_dates.append({"label": str(label), "date": str(date_val)})
            else:
                key_dates.append({"label": str(item), "date": ""})
    if not key_dates:
        key_dates = [
            {"label": "投标截止", "date": "待定"},
            {"label": "开标时间", "date": "待定"},
            {"label": "答疑截止", "date": "待定"},
        ]

    # documentStructure 兼容 dict / list，sections 兼容 content/details 等字段
    raw_struct = parsed.get("documentStructure", [])
    if isinstance(raw_struct, dict):
        doc_struct_list = [raw_struct]
    elif isinstance(raw_struct, list):
        doc_struct_list = raw_struct
    else:
        doc_struct_list = []

    def normalize_sections(sec: any) -> list[str]:
        if sec is None:
            return []
        if isinstance(sec, list):
            out: list[str] = []
            for s in sec:
                if isinstance(s, dict):
                    # 兼容 content/details/value/title
                    if "content" in s and isinstance(s["content"], list):
                        out.extend([str(x.get("value") if isinstance(x, dict) else x) for x in s["content"]])
                    elif "details" in s and isinstance(s["details"], list):
                        out.extend([str(x.get("value") if isinstance(x, dict) else x) for x in s["details"]])
                    else:
                        out.append(str(s.get("value") or s.get("title") or s.get("text") or s))
                else:
                    out.append(str(s))
            return out
        if isinstance(sec, dict):
            return [str(sec.get("value") or sec.get("title") or sec.get("text") or sec)]
        return [str(sec)]

    doc_struct: list[dict] = []
    for ch in doc_struct_list:
        if isinstance(ch, dict):
            title = ch.get("title") or ch.get("heading") or ch.get("id") or "章节"
            sections_field = ch.get("sections") or ch.get("content") or ch.get("details") or []
            doc_struct.append(
                {
                    "id": str(ch.get("id") or title),
                    "title": str(title),
                    "sections": normalize_sections(sections_field),
                }
            )
        else:
            doc_struct.append({"id": str(ch), "title": str(ch), "sections": []})

    if not doc_struct:
        doc_struct = [
            {"id": "overview", "title": "1. 公司概况", "sections": ["企业简介", "核心优势", "{{material:company_intro}}"]},
            {"id": "solution", "title": "2. 技术方案", "sections": ["总体设计", "关键技术", "实施路径", "{{material:solution_detail}}"]},
            {"id": "team", "title": "3. 项目团队", "sections": ["组织架构", "关键岗位", "{{material:team_resume}}"]},
            {"id": "case", "title": "4. 成功案例", "sections": ["案例概览", "{{material:case_study}}"]},
            {"id": "service", "title": "5. 服务与保障", "sections": ["服务承诺", "质保与培训", "{{material:service_plan}}"]},
        ]

    # 不再因模型格式问题中断，记录日志后继续返回结果
    raw_preview = str(llm_resp) if llm_resp is not None else "<no-response>"
    if len(raw_preview) > 800:
        raw_preview = raw_preview[:800] + "...(truncated)"
    if not summary.strip() or summary.strip() == "暂无模型总结，请检查招标文件与模型输出。":
        logger.warning("LLM输出为空或占位，使用占位 summary | raw=%s", raw_preview)

    if record:
        record.summary = summary
        record.key_dates_json = json.dumps(key_dates, ensure_ascii=False)
        record.document_structure_json = json.dumps(doc_struct, ensure_ascii=False)
        new_record = record
    else:
        new_record = TenderAnalysisModel(
            project_id=project_id,
            summary=summary,
            key_dates_json=json.dumps(key_dates, ensure_ascii=False),
            document_structure_json=json.dumps(doc_struct, ensure_ascii=False),
        )
    db.add(new_record)

    # 初始化结构：仅在正文不存在时补充 structure 字段，避免覆盖生成的正文内容
    doc_content = db.query(DocumentContent).filter(DocumentContent.project_id == project_id).first()
    try:
        existing = json.loads(doc_content.content_json) if doc_content and doc_content.content_json else {}
    except Exception:
        existing = {}

    if isinstance(existing, list):
        existing = {"content": existing, "structure": existing}

    if not existing.get("content"):
        existing["structure"] = doc_struct
        if not doc_content:
            doc_content = DocumentContent(project_id=project_id)
        doc_content.content_json = json.dumps(existing, ensure_ascii=False)
        db.add(doc_content)
        db.commit()

    return TenderAnalysis(
        summary=summary,
        keyDates=key_dates,
        documentStructure=doc_struct,
    )

def extract_key_info_with_ollama(raw_text: str) -> dict:
    """
    Use local Ollama model to extract key tender information
    for downstream knowledge-base querying.
    """
    if not raw_text or not raw_text.strip():
        return {}

    prompt = f"""
    你是专业的招投标文件关键信息抽取器，擅长从政府或企业招标文件中提取
    “可用于投标经验检索、方案对齐和风险判断”的核心信息。

    请严格基于招标文件原文内容进行提取：
    - 不要臆测
    - 不要补充文件中未明确说明的信息
    - 不要使用泛化或空洞表述（如“需满足要求”“方案合理”等）

    只输出 JSON，不要解释，不要 Markdown，不要输出无关文本。

    字段说明与提取要求如下：

    - project_type：
    用一个简短、通用的项目类型名称概括本项目，
    例如：网络安全运营服务、信息化系统建设、安防工程等。
    不要使用完整项目名称或长句。

    - core_tech：
    列出招标文件中明确要求的关键技术或服务能力，
    使用关键词或短语形式，例如：
    “安全运营（SOC）”、“7×24 监测”、“应急响应”、“日志分析”、“态势感知”等。
    不要包含泛化描述。

    - qualification：
    列出投标人或项目人员必须满足的资质、证书、业绩或人数要求，
    重点提取“不满足可能导致废标或明显扣分”的条件。

    - scoring_focus：
    提取评分办法或评审标准中，明确影响得分的重点因素，
    例如：技术方案完整性、类似项目经验、人员配置、安全合规能力等。

    - risk_points：
    仅列出可以从文件中直接判断出的废标风险或重大扣分风险，
    例如：强制资质要求、人员不到位、不接受联合体等。
    如果文件中未体现明显风险点，可返回空数组。

    如果某一字段在文件中未明确体现，请返回空字符串或空数组，不要猜测。

    招标文件原文如下：
    {raw_text}
    """

    try:
        resp = _call_ollama(prompt)  # 本地 Ollama 模型调用

        logger.warning(
            "[Ollama] raw response preview:\n%s",
            str(resp)[:1500] if resp else "<empty>"
        )

        parsed = _parse_llm_json(resp)
        return parsed if isinstance(parsed, dict) else {}
    except Exception as exc:
        logger.warning("ollama key info extraction failed: %s", exc)
        return {}


def build_anythingllm_queries(extracted: dict, project_name: str) -> list[str]:
    """
    Build targeted AnythingLLM queries based on extracted key info.
    """
    if not extracted:
        return []

    queries: list[str] = []

    project_type = extracted.get("project_type")
    core_tech = extracted.get("core_tech", [])
    qualification = extracted.get("qualification", [])
    scoring_focus = extracted.get("scoring_focus", [])
    risk_points = extracted.get("risk_points", [])

    if project_type:
        queries.append(f"{project_type} 招投标 常见 技术评分 要点")
        queries.append(f"{project_type} 项目 废标 常见 原因")

    if qualification:
        queries.append(
            f"{project_type or ''} 资质审查 风险 {' '.join(qualification)}"
        )

    if core_tech:
        queries.append(
            f"{project_type or ''} {' '.join(core_tech)} 技术方案 投标 经验"
        )

    if scoring_focus:
        queries.append(
            f"{project_type or ''} 评分重点 {' '.join(scoring_focus)}"
        )

    # 兜底：至少有一个 query
    if not queries:
        queries.append(f"{project_name} 招投标 经验 要点")

    return queries


@router.post("/{project_id}", response_model=TenderAnalysis)
def analyze(project_id: int, refresh: bool = Query(False), db: Session = Depends(get_db)):
    return _analyze_core(project_id, db, refresh=refresh)


@router.get("/{project_id}", response_model=TenderAnalysis)
def get_analysis(project_id: int, refresh: bool = Query(False), db: Session = Depends(get_db)):
    # 读已存在；如无则即时生成，便于前端通过 GET 直接取数。
    return _analyze_core(project_id, db, refresh=refresh)

