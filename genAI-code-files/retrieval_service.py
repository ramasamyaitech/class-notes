from langchain_community.vectorstores import FAISS

from models import OllamaModel
from utils.config import settings


class RetrievalService:

    def __init__(self):

        self.model = OllamaModel()

        self.embeddings = self.model.get_embeddings()

        self.vector_store = None

        self.load_vector_store()

    def load_vector_store(self):

        self.vector_store = FAISS.load_local(
            settings.VECTOR_DB_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

    def retrieve(self, query: str):

        documents = self.vector_store.similarity_search(
            query,
            k=settings.TOP_K
        )

        return documents