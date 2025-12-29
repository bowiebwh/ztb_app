import io
import os
from typing import List
from PyPDF2 import PdfReader
from docx import Document


def chunk_text(text: str, max_tokens: int = 800) -> List[str]:
    words = text.split()
    chunks = []
    current = []
    count = 0
    for w in words:
        current.append(w)
        count += 1
        if count >= max_tokens:
            chunks.append(" ".join(current))
            current = []
            count = 0
    if current:
        chunks.append(" ".join(current))
    return chunks


def parse_pdf(data: bytes) -> List[str]:
    reader = PdfReader(io.BytesIO(data))
    text_parts = []
    for page in reader.pages:
        try:
            text_parts.append(page.extract_text() or "")
        except Exception:
            continue
    full_text = "\n".join(text_parts)
    return chunk_text(full_text)


def parse_docx(data: bytes) -> List[str]:
    with open(".__tmp_upload.docx", "wb") as f:
        f.write(data)
    doc = Document(".__tmp_upload.docx")
    paras = [p.text for p in doc.paragraphs if p.text]
    full_text = "\n".join(paras)
    try:
        os.remove(".__tmp_upload.docx")
    except Exception:
        pass
    return chunk_text(full_text)


def parse_text(data: bytes) -> List[str]:
    return chunk_text(data.decode("utf-8", errors="ignore"))


def parse_file_bytes(filename: str, data: bytes) -> List[str]:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return parse_pdf(data)
    if lower.endswith(".docx") or lower.endswith(".doc"):
        return parse_docx(data)
    return parse_text(data)
