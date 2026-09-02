from app.rag.query_rewriter import rewrite_query


def test_rewrite_query_uses_history():
    history = (
        "User: Can employees work remotely?\n"
        "Assistant: Yes, employees may work remotely according "
        "to their team's remote work policy."
    )

    rewritten = rewrite_query(
        query="What about their managers?",
        history=history,
    )

    assert rewritten
    assert "remote" in rewritten.lower()
    assert "manager" in rewritten.lower()