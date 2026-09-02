from app.rag.llm import generate_text


QUERY_REWRITE_PROMPT = """
Rewrite the user's latest question into a standalone question that can be
used for document retrieval.

Use the conversation history to resolve references such as:
- "they"
- "their"
- "it"
- "that"
- "what about them"

Rules:
1. Preserve the meaning of the user's latest question.
2. Do not answer the question.
3. Do not add information that is not present in the conversation.
4. Return only the rewritten standalone question.
""".strip()


def rewrite_query(
    query: str,
    history: str,
) -> str:
    if not history:
        return query

    prompt = f"""SYSTEM:

{QUERY_REWRITE_PROMPT}

CONVERSATION HISTORY:

{history}

LATEST USER QUESTION:

{query}

STANDALONE RETRIEVAL QUESTION:

"""

    rewritten_query = generate_text(prompt)

    return rewritten_query.strip()