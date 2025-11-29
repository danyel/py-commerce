from fastapi.testclient import TestClient
from run import app

client = TestClient(app)

def test_create_item():
    response = client.post("/api/ping")
    assert response.status_code == 200
    assert response.json()["name"] == "name"
    assert response.json()["status"] == "ok"
