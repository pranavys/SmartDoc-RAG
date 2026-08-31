from app.db.database import SessionLocal
from app.db.repository import search_similar_chunks
from app.rag.embeddings import generate_embedding
from app.rag.reranker import rerank


def retrieve_chunks(
    query: str,
    limit: int = 5,
):
    query_embedding = generate_embedding(query)

    db = SessionLocal()

    try:
        chunks = search_similar_chunks(
            db=db,
            query_embedding=query_embedding,
            limit=limit,
        )

        return chunks

    finally:
        db.close()


def retrieve_and_rerank(
    query: str,
    retrieval_limit: int = 5,
    rerank_limit: int = 3,
):
    chunks = retrieve_chunks(
        query=query,
        limit=retrieval_limit,
    )

    ranked_chunks = rerank(
        query=query,
        chunks=chunks,
        top_k=rerank_limit,
    )

    return ranked_chunks