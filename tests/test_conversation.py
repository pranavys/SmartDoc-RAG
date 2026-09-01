from app.rag.service import answer_question


def test_conversation_keeps_same_conversation_id():
    conversation_id, first_answer = answer_question(
        query="How many vacation days do employees get?"
    )

    assert conversation_id is not None
    assert first_answer

    second_conversation_id, second_answer = answer_question(
        query="Can employees work remotely?",
        conversation_id=conversation_id,
    )

    assert second_conversation_id == conversation_id
    assert second_answer