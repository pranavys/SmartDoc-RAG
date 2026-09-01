from app.rag.retriever import retrieve_and_rerank


def get_relevant_context(
    query: str,
    retrieval_limit: int = 5,
    rerank_limit: int = 3,
) -> str:
    results = retrieve_and_rerank(
        query=query,
        retrieval_limit=retrieval_limit,
        rerank_limit=rerank_limit,
    )

    if not results:
        return ""

    context_parts = []

    for chunk, score in results:
        context_parts.append(chunk.content)

    return "\n\n".join(context_parts)