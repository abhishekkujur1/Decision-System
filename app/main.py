from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from .workflow_engine import WorkflowEngine
from .state_manager import StateManager
from .audit_logger import AuditLogger

app = FastAPI(title="Configurable Workflow Decision Platform")

# Shared in-memory DB components
state_mgr = StateManager()
audit_mgr = AuditLogger()
engine = WorkflowEngine(state_mgr, audit_mgr)

class WorkflowRequest(BaseModel):
    request_id: str
    workflow_type: str
    data: Dict[str, Any]

@app.post("/request")
def submit_request(req: WorkflowRequest):
    result = engine.process(req.request_id, req.workflow_type, req.data)
    return result

@app.get("/status/{request_id}")
def get_status(request_id: str):
    state = state_mgr.get_state(request_id)
    if not state:
        raise HTTPException(status_code=404, detail="Request not found")
    return state

@app.get("/audit/{request_id}")
def get_audit_logs(request_id: str):
    logs = audit_mgr.get_logs(request_id)
    return {"request_id": request_id, "logs": logs}
