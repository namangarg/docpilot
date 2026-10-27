from app.routers import documents, search
from fastapi import FastAPI

app = FastAPI(title="DocPilot")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(documents.router)
app.include_router(search.router)