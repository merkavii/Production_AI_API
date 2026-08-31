from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    res_json = response.json()
    assert response.status_code == 200
    assert res_json['status'] == 'healthy'
    
    