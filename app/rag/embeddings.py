import ollama

from app.core.config import settings


def generate_embedding(text: str) -> list[float]:
    response = ollama.embed(
        model=settings.embedding_model,
        input=text,
    )

    return response["embeddings"][0]