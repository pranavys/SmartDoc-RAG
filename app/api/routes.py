from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.service import answer_question


router = APIRouter()


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