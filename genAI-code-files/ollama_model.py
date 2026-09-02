from langchain_ollama import ChatOllama, OllamaEmbeddings

from utils.config import settings


class OllamaModel:

    def get_llm(self):

        return ChatOllama(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0
        )

    def get_embeddings(self):

        return OllamaEmbeddings(
            model=settings.EMBEDDING_MODEL,
            base_url=settings.OLLAMA_BASE_URL
        )