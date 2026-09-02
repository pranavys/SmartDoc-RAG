from app.db.database import SessionLocal
from app.db.repository import (
    add_message,
    create_conversation,
    get_conversation_messages,
)
from app.rag.context import get_relevant_context
from app.rag.history import format_history
from app.rag.llm import generate_answer
from app.rag.prompts import build_prompt
from app.rag.query_rewriter import rewrite_query


def answer_question(
    query: str,
    conversation_id: int | None = None,
) -> tuple[int, str]:

    db = SessionLocal()

    try:
        # Create a new conversation if needed
        if conversation_id is None:
            conversation = create_conversation(db)
            conversation_id = conversation.id

        # Get previous conversation history
        messages = get_conversation_messages(
            db,
            conversation_id,
        )

        history = format_history(messages)

        # Rewrite the query using conversation history
        retrieval_query = rewrite_query(
            query=query,
            history=history,
        )

        # Retrieve and rerank relevant documents
        context = get_relevant_context(
            query=retrieval_query,
            retrieval_limit=5,
            rerank_limit=3,
        )

        # Build final prompt
        prompt = build_prompt(
            query=query,
            context=context,
            history=history,
        )

        # Generate answer
        answer = generate_answer(prompt)

        # Save user message
        add_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=query,
        )

        # Save assistant message
        add_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
        )

        return conversation_id, answer

    finally:
        db.close()