from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from models import OllamaModel
from utils.config import settings


class IngestionService:

    def __init__(self):

        self.model = OllamaModel()

        self.embeddings = self.model.get_embeddings()

    def load_pdf(self, file_path: str):

        loader = PyPDFLoader(file_path)

        documents = loader.load()

        return documents

    def split_documents(self, documents):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

        chunks = splitter.split_documents(documents)

        return chunks

    def create_vector_store(self, chunks):

        vector_store = FAISS.from_documents(
            chunks,
            self.embeddings
        )

        vector_store.save_local(
            settings.VECTOR_DB_PATH
        )

        return vector_store

    def ingest(self, file_path: str):

        documents = self.load_pdf(file_path)

        print(f"Loaded documents: {len(documents)}")

        chunks = self.split_documents(documents)

        print(f"Created chunks: {len(chunks)}")

        vector_store = self.create_vector_store(chunks)

        print("Vector store created successfully.")

        return vector_store