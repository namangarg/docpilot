from typing import Annotated, TypeAlias

from app.services.llm import FakeLLM, LLMProvider
from app.services.store import DocumentStore
from fastapi import Depends

_store = DocumentStore()
_llm = FakeLLM()

def get_store() -> DocumentStore:
    return _store

def get_llm() -> LLMProvider:
    return _llm


StoreDep = Annotated[DocumentStore, Depends(get_store)]
LLMDep: TypeAlias = Annotated[LLMProvider, Depends(get_llm)]

