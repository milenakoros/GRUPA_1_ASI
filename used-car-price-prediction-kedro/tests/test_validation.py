from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_validation_error():
    response = client.post("/predict", json={"feature_num": "oops", "feature_cat": "A"})
    assert response.status_code == 422
