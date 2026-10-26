import uuid
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="DocPilot")
documents: dict[str, dict] = {}

class DocumentCreate(BaseModel):
    title: str = Field(min_length = 1,max_length = 200)
    text: str = Field(min_length = 1)

class DocumentOut(BaseModel):
    id: str
    title: str
    created_at: datetime


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/documents", response_model = DocumentOut, status_code=201)
def create_document(body: DocumentCreate):
    doc = {
        "id": uuid.uuid4().hex,
        "title": body.title,
        "text": body.text,
        "created_at": datetime.now(UTC) 
    }
    documents[doc["id"]] = doc
    return doc

@app.get("/documents", response_model=list[DocumentOut])
def list_documents():
    return list(documents.values())

@app.get("/documents/{doc_id}", response_model=DocumentOut)
def get_document(doc_id: str):
    doc = documents.get(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@app.delete("/documents/{doc_id}", status_code=204)
def delete_document(doc_id: str):
    if documents.pop(doc_id, None) is None:
        raise HTTPException(status_code=404, detail="Document not found")

    