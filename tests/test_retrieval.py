from app.rag.retriever import retrieve_and_rerank


def test_retrieve_and_rerank_returns_results():
    query = "How many vacation days do employees get?"

    results = retrieve_and_rerank(
        query=query,
        retrieval_limit=5,
        rerank_limit=3,
    )

    assert results
    assert len(results) <= 3

    for chunk, score in results:
        assert chunk.content
        assert isinstance(chunk.content, str)
        assert isinstance(score, (int, float))