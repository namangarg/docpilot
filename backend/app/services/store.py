import uuid
from datetime import UTC, datetime

from app.services.chunking import chunk_text

CHUNK_SIZE = 120     # words per chunk
CHUNK_OVERLAP = 20   # words shared between neighbouring chunks

class DocumentStore:
    def __init__(self):
        self.docs: dict[str, dict] = {}

    def add(self, title: str, text: str) -> dict:
        doc_id = str(uuid.uuid4())
        doc = {
            "id": doc_id,
            "title": title,
            "text": text,
            "chunks": chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP),
            "created_at": datetime.now(UTC),
        }
        self.docs[doc_id] = doc
        return doc

    def list_all(self) -> list[dict]:
        return list(self.docs.values())

    def get(self, doc_id: str) -> dict | None:
        return self.docs.get(doc_id)

    def delete(self, doc_id: str) -> bool:
        return self.docs.pop(doc_id, None) is not None
   