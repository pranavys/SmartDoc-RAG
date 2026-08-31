from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str

    ollama_base_url: str = "http://localhost:11434"

    llm_model: str = "gemma3:4b"

    embedding_model: str = "embeddinggemma"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()