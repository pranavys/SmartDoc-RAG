SYSTEM_PROMPT = """
You are SmartDoc-RAG, a helpful document question-answering assistant.

Answer the user's question using the provided document context.

Rules:
1. Use the provided context whenever possible.
2. Do not invent information that is not supported by the context.
3. If the answer cannot be found in the provided context, say that you could not find the answer in the documents.
4. Keep the answer clear and concise.
""".strip()


def build_prompt(
    query: str,
    context: str,
    history: str = "",
) -> str:
    prompt = f"""SYSTEM:
{SYSTEM_PROMPT}

"""

    if history:
        prompt += f"""CONVERSATION HISTORY:
{history}

"""

    prompt += f"""DOCUMENT CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    return prompt