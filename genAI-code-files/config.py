# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):

#     OLLAMA_BASE_URL: str = "http://localhost:11434"

#     LLM_MODEL: str = "llama3.2:1b"
#     EMBEDDING_MODEL: str = "nomic-embed-text"

#     VECTOR_DB_PATH: str = "data/vectorstore"

#     CHUNK_SIZE: int = 800
#     CHUNK_OVERLAP: int = 150

#     TOP_K: int = 2
#     SIMILARITY_THRESHOLD: float = 0.4

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         extra="ignore"
#     )


# settings = Settings()


# ===================================


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    OLLAMA_BASE_URL: str
    LLM_MODEL: str
    EMBEDDING_MODEL: str

    VECTOR_DB_PATH: str

    CHUNK_SIZE: int
    CHUNK_OVERLAP: int

    TOP_K: int
    SIMILARITY_THRESHOLD: float

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

