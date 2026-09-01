from app.rag.context import get_relevant_context
from app.rag.llm import generate_answer
from app.rag.prompts import build_prompt


def answer_question(
    query: str,
    history: str = "",
) -> str:

    context = get_relevant_context(
        query=query,
        retrieval_limit=5,
        rerank_limit=3,
    )

    prompt = build_prompt(
        query=query,
        context=context,
        history=history,
    )

    answer = generate_answer(prompt)

    return answer