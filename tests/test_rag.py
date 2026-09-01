from app.rag.service import answer_question


def test_rag_returns_answer_from_documents():
    query = "How many days of annual leave do employees receive?"

    conversation_id, answer = answer_question(
        query=query,
    )

    assert conversation_id is not None
    assert answer
    assert "30 days" in answer