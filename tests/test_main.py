from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_happy_path():
    req_id = str(uuid.uuid4())
    payload = {
        "request_id": req_id,
        "workflow_type": "application_approval",
        "data": {"doc_id": "123", "requested_amount": 10000}
    }
    response = client.post("/request", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"

def test_rule_branching_manual_review():
    req_id = str(uuid.uuid4())
    payload = {
        "request_id": req_id,
        "workflow_type": "application_approval",
        "data": {"doc_id": "123", "requested_amount": 90000} # Exceeds 50k threshold
    }
    response = client.post("/request", json=payload)
    assert response.json()["status"] == "MANUAL_REVIEW"

def test_idempotency():
    req_id = "duplicate_id_123"
    payload = {"request_id": req_id, "workflow_type": "application_approval", "data": {}}
    client.post("/request", json=payload)
    
    # Second request with same ID
    response = client.post("/request", json=payload)
    assert response.json()["message"] == "Idempotent request. Already processed."