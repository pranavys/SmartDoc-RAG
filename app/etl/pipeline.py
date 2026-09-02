from pathlib import Path

from app.db.database import SessionLocal
from app.db.repository import (
    create_document,
    create_document_chunk,
    get_document_by_filename,
)
from app.etl.extractor import extract_document
from app.etl.transformer import clean_text, chunk_text
from app.rag.embeddings import generate_embedding


def process_document(file_path: str) -> list[str]:
    # Extract
    raw_text = extract_document(file_path)

    # Transform
    cleaned_text = clean_text(raw_text)
    # chunks = chunk_text(cleaned_text)
    chunks = chunk_text(
    cleaned_text,
    chunk_size=200,
    chunk_overlap=30,
)

    return chunks


def ingest_document(file_path: str) -> None:
    # Extract
    raw_text = extract_document(file_path)

    # Transform
    cleaned_text = clean_text(raw_text)

    chunks = chunk_text(
        cleaned_text,
        chunk_size=200,
        chunk_overlap=30,
    )

    # Load
    db = SessionLocal()

    try:
        filename = Path(file_path).name

        existing_document = get_document_by_filename(
            db=db,
            filename=filename,
        )

        if existing_document:
            return

        document = create_document(
            db=db,
            filename=filename,
        )

        for index, chunk in enumerate(chunks):
            embedding = generate_embedding(chunk)

            create_document_chunk(
                db=db,
                document_id=document.id,
                chunk_index=index,
                content=chunk,
                embedding=embedding,
            )

    finally:
        db.close()