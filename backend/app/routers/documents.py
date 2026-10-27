from app.deps import StoreDep
from app.schemas import DocumentCreate, DocumentOut
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentOut, status_code=201)
def create_document(body: DocumentCreate, store: StoreDep):
    return store.add(body.title, body.text)


@router.get("", response_model=list[DocumentOut])
def list_documents(store: StoreDep):
    return store.list_all()


@router.get("/{doc_id}", response_model=DocumentOut)
def get_document(doc_id: str, store: StoreDep):
    doc = store.get(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.delete("/{doc_id}", status_code=204)
def delete_document(doc_id: str, store: StoreDep):
    if not store.delete(doc_id):
        raise HTTPException(status_code=404, detail="Document not found")