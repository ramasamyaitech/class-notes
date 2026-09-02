from fastapi import FastAPI

from api import router


app = FastAPI(
    title="Enterprise RAG Application",
    version="1.0.0"
)


app.include_router(
    router,
    prefix="/api"
)


@app.get("/")
def root():

    return {
        "application": "RAG Application",
        "status": "running"
    }