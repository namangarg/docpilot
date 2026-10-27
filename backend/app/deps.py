from typing import Annotated

from app.services.store import DocumentStore
from fastapi import Depends

_store = DocumentStore()


def get_store() -> DocumentStore:
    return _store


StoreDep = Annotated[DocumentStore, Depends(get_store)]