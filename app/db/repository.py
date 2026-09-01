from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import (
    Conversation,
    Document,
    DocumentChunk,
    Message,
)

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

def search_similar_chunks(
    db: Session,
    query_embedding: list[float],
    limit: int = 5,
) -> list[DocumentChunk]:
    statement = (
        select(DocumentChunk)
        .order_by(
            DocumentChunk.embedding.cosine_distance(query_embedding)
        )
        .limit(limit)
    )

    return list(db.scalars(statement).all())

def create_conversation(db: Session) -> Conversation:
    conversation = Conversation()

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def add_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_conversation_messages(
    db: Session,
    conversation_id: int,
) -> list[Message]:
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )

    return list(db.scalars(statement).all())