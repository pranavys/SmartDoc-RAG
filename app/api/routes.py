from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, field_validator
from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models import Conversation, Document
from app.etl.pipeline import ingest_document
from app.rag.service import answer_question


router = APIRouter()

RAW_DATA_DIR = Path("data/raw")


class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty.")

        return value


class ChatResponse(BaseModel):
    conversation_id: int
    answer: str


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    db = SessionLocal()

    try:
        if request.conversation_id is not None:

            conversation = db.scalar(
                select(Conversation).where(
                    Conversation.id == request.conversation_id
                )
            )

            if conversation is None:
                raise HTTPException(
                    status_code=404,
                    detail="Conversation not found.",
                )

        conversation_id, answer = answer_question(
            query=request.message,
            conversation_id=request.conversation_id,
        )

        return ChatResponse(
            conversation_id=conversation_id,
            answer=answer,
        )

    except HTTPException:
        raise

    except Exception as error:
        print(f"Chat error: {error}")

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question.",
        )

    finally:
        db.close()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    allowed_extensions = {".pdf", ".docx"}

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was selected.",
        )

    filename = Path(file.filename).name
    file_extension = Path(filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = RAW_DATA_DIR / filename

    db = SessionLocal()

    try:

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

    try:

        with open(file_path, "wb") as output_file:
            output_file.write(file_content)

        ingest_document(str(file_path))

    except Exception as error:

        if file_path.exists():
            file_path.unlink()

        print(f"Upload error: {error}")

        raise HTTPException(
            status_code=500,
            detail="The document could not be processed.",
        )

    return {
        "message": "Document uploaded and processed successfully.",
        "filename": filename,
    }