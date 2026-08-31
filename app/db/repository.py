from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk


def create_document(
    db: Session,
    filename: str,
) -> Document:
    document = Document(filename=filename)

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def create_document_chunk(
    db: Session,
    document_id: int,
    chunk_index: int,
    content: str,
    embedding: list[float],
) -> DocumentChunk:
    chunk = DocumentChunk(
        document_id=document_id,
        chunk_index=chunk_index,
        content=content,
        embedding=embedding,
    )

    db.add(chunk)
    db.commit()
    db.refresh(chunk)

    return chunk