from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.etl.pipeline import ingest_document
from app.rag.service import answer_question
from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models import Document


router = APIRouter()

RAW_DATA_DIR = Path("data/raw")


class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None


class ChatResponse(BaseModel):
    conversation_id: int
    answer: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    conversation_id, answer = answer_question(
        query=request.message,
        conversation_id=request.conversation_id,
    )

    return ChatResponse(
        conversation_id=conversation_id,
        answer=answer,
    )


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".docx"}

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    filename = Path(file.filename).name
    file_path = RAW_DATA_DIR / filename

    db = SessionLocal()

    try:
        # Check whether this document already exists
        statement = select(Document).where(
            Document.filename == filename
        )

        existing_document = db.scalar(statement)

        if existing_document:
            return {
                "message": "Document already exists.",
                "filename": filename,
            }

    finally:
        db.close()

    # Save the new file
    file_content = await file.read()

    with open(file_path, "wb") as output_file:
        output_file.write(file_content)

    # Run the existing ETL + embedding + database pipeline
    ingest_document(str(file_path))

    return {
        "message": "Document uploaded and processed successfully.",
        "filename": filename,
    }