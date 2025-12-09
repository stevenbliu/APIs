from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user_http():
    resp = client.post("/api/users/", json={...})
    assert resp.status_code == 200
