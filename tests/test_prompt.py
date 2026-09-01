from app.rag.prompts import build_prompt


def test_build_prompt_contains_context_and_question():
    context = "Employees receive 30 days of annual leave."
    query = "How many days of annual leave do employees receive?"

    prompt = build_prompt(
        query=query,
        context=context,
    )

    assert context in prompt
    assert query in prompt