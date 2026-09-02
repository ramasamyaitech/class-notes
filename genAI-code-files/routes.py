from fastapi import APIRouter, UploadFile, File

from schemas import ChatRequest, ChatResponse
from services import IngestionService
from services.rag_service import RAGService


router = APIRouter()

ingestion_service = IngestionService()


@router.get("/health")
def health():

    return {
        "status": "UP",
        "message": "RAG API is running"
    }


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):

    file_path = f"data/documents/{file.filename}"

    with open(file_path, "wb") as buffer:

        buffer.write(await file.read())

    ingestion_service.ingest(file_path)

    return {
        "message": "Document ingested successfully",
        "file": file.filename
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    rag_service = RAGService()

    result = rag_service.ask(
        request.question
    )

    return result