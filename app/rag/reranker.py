from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker = CrossEncoder(MODEL_NAME)


def rerank(
    query: str,
    chunks: list,
    top_k: int = 3,
) -> list:
    if not chunks:
        return []

    pairs = [
        [query, chunk.content]
        for chunk in chunks
    ]

    scores = reranker.predict(pairs)

    ranked_chunks = sorted(
        zip(chunks, scores),
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        (chunk, float(score))
        for chunk, score in ranked_chunks[:top_k]
    ]