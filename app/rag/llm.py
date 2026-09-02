import os

from ollama import Client


MODEL_NAME = os.getenv("LLM_MODEL", "gemma3:4b")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

client = Client(host=OLLAMA_BASE_URL)


def generate_text(prompt: str) -> str:
    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]


def generate_answer(prompt: str) -> str:
    return generate_text(prompt)