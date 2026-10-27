from app.deps import StoreDep
from app.services.retrieval import search
from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter(tags=["search"])


class SearchHit(BaseModel):
    document_id: str
    document_title: str
    chunk_index: int
    text: str
    score: float

@router.get("/search", response_model=list[SearchHit])
def search_documents(
    store: StoreDep,
    q: str = Query(min_length=1),
    top_k: int = Query(default=4, gt=0, le=100),
):
    return search(store.list_all(), q, top_k)