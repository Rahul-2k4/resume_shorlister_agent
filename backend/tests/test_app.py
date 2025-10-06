from fastapi.testclient import TestClient

from backend.app import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"].startswith("AI-Powered Resume Screening")
    assert "upload" in payload["endpoints"]
