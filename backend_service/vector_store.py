from typing import List, Tuple
from sqlalchemy.orm import Session
from models import DocumentChunk

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except Exception:
    TfidfVectorizer = None
    cosine_similarity = None


def search_chunks(db: Session, project_id: int, query: str, top_k: int = 5) -> List[Tuple[int, str, float]]:
    """
    返回 [(chunk_id, content, score), ...]
    """
    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.project_id == project_id)
        .order_by(DocumentChunk.created_at.desc())
        .all()
    )
    if not chunks:
        return []

    texts = [c.content for c in chunks]

    if not TfidfVectorizer or not cosine_similarity:
        # Fallback: 简单关键词命中计数
        scores = []
        for c in chunks:
            score = sum(query.lower().count(w) for w in c.content.lower().split())
            scores.append(score)
        ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)[:top_k]
        return [(c.id, c.content, float(s)) for c, s in ranked]

    vectorizer = TfidfVectorizer(max_features=5000)
    tfidf = vectorizer.fit_transform(texts)
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, tfidf).flatten()
    ranked_idx = sims.argsort()[::-1][:top_k]
    results = []
    for idx in ranked_idx:
        results.append((chunks[idx].id, chunks[idx].content, float(sims[idx])))
    return results
