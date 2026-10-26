import pytest
from fastapi.testclient import TestClient
from main import app, documents

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_store():
    documents.clear()


def create(title="Policy", text="Refunds within 14 days."):
    return client.post("/documents", json={"title": title, "text": text})


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_returns_201_and_hides_text():
    r = create()
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Policy"
    assert "id" in body
    assert "text" not in body


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "", "text": "x"},
        {"title": "t"},
        {"title": "t" * 201, "text": "x"},
    ],
)
def test_create_validation_errors(payload):
    assert client.post("/documents", json=payload).status_code == 422


def test_list_documents():
    create("A")
    create("B")
    r = client.get("/documents")
    assert r.status_code == 200
    assert {d["title"] for d in r.json()} == {"A", "B"}


def test_get_document():
    doc_id = create().json()["id"]
    r = client.get(f"/documents/{doc_id}")
    assert r.status_code == 200
    assert r.json()["id"] == doc_id


def test_get_unknown_document_is_404():
    assert client.get("/documents/nope").status_code == 404


def test_delete_document():
    doc_id = create().json()["id"]
    assert client.delete(f"/documents/{doc_id}").status_code == 204
    assert client.get(f"/documents/{doc_id}").status_code == 404
    assert client.delete(f"/documents/{doc_id}").status_code == 404