# Configurable Workflow Decision Platform

## Overview
A resilient platform built to handle real-world business workflows under ambiguity, changing requirements, and operational constraints. It evaluates configurable rules, manages state, handles failures, and provides full audit logs.

## Setup & Running Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Start the server: `uvicorn app.main:app --reload`
3. Run tests: `pytest tests/`

## API Usage Examples
**Submit Request:**
`POST http://localhost:8000/request`
```json
{
  "request_id": "req-001",
  "workflow_type": "application_approval",
  "data": {"doc_id": "abc", "requested_amount": 60000}
}