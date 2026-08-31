from app.db.database import SessionLocal
from app.db.repository import search_similar_chunks
from app.rag.embeddings import generate_embedding


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