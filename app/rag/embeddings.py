import os

from ollama import Client

from app.core.config import settings


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

client = Client(host=OLLAMA_BASE_URL)


def generate_embedding(text: str) -> list[float]:
    response = client.embed(
        model=settings.embedding_model,
        input=text,
    )

    return response["embeddings"][0]