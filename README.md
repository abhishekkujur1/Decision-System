# Configurable Workflow Decision Platform

## Project Overview
This project implements a resilient, configurable workflow decision platform designed to handle real-world business workflows under ambiguity, changing requirements, and operational constraints.

The system processes structured incoming requests, evaluates configurable business rules, executes workflow stages, maintains request state, and ensures full traceability through comprehensive audit logs.

The platform is built using Python and FastAPI, demonstrating backend engineering principles such as modular architecture, configuration-driven logic, idempotent processing, and robust failure handling.

---

## Core Features

### Input Intake & Validation
Accepts structured REST API requests and validates the input schema before processing.

### Dynamic Rule Evaluation
Supports business rules such as threshold checks, conditional branching, and mandatory checks.  
Rules are configurable through JSON files without requiring code changes.

### Configurable Workflow Execution
Workflow stages such as success, rejection, retries, and manual review are executed dynamically based on rule evaluation.

### Resilient State & Failure Handling
The system ensures:

- Idempotency (duplicate request protection)
- Retry logic for external dependency failures
- Robust state tracking throughout the workflow lifecycle

### Comprehensive Auditability
Every decision is fully explainable through:

- Input data
- Triggered rules
- Final decision
- Timestamped audit trail

---

## System Architecture

The system follows a modular architecture with clear separation of concerns.

```
Client
   │
   ▼
FastAPI API Layer
   │
   ▼
Workflow Engine
   │
   ▼
Rule Engine
   │
   ▼
State Manager
   │
   ▼
Audit Logger
```

### Component Responsibilities

| Component | Responsibility |
|----------|---------------|
| API Layer | Accepts requests and validates input |
| Workflow Engine | Orchestrates workflow execution |
| Rule Engine | Evaluates configurable business rules |
| State Manager | Maintains request lifecycle and idempotency |
| Audit Logger | Records rule traces and decision logs |

---

## Project Folder Structure

```
Decision-System/
├── app/
│   ├── __init__.py
│   ├── audit_logger.py
│   ├── external_service.py
│   ├── main.py
│   ├── rule_engine.py
│   ├── state_manager.py
│   └── workflow_engine.py
│
├── config/
│   ├── rules.json
│   └── workflow.yaml
│
├── tests/
│   ├── test_main.py
│
├── pytest.ini
├── README.md
└── requirements.txt
```

The architecture ensures modularity, maintainability, and extensibility.

---

## Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- Pytest

Install dependencies using:

```
pip install -r requirements.txt
```

---

## How to Run the Project

### Clone the Repository

```
git clone <repository_url>
cd Decision-System
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Start the Server

```
uvicorn app.main:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

---

## Running Tests

Execute the test suite using:

```
pytest tests/
```

The test suite validates:

- Happy path workflow execution
- Rule branching logic
- Idempotent request handling
- Dependency failure handling
- Retry flows

---

## API Endpoints

### Submit Request

Endpoint

```
POST /request
```

Example Request

```json
{
  "request_id": "req-1001",
  "workflow_type": "application_approval",
  "data": {
    "doc_id": "DOC-99",
    "requested_amount": 60000
  }
}
```

Example Response

```json
{
  "request_id": "req-1001",
  "status": "MANUAL_REVIEW",
  "decision": {
    "status": "MANUAL_REVIEW",
    "triggered": ["High Risk Flag"],
    "reason": "Risk threshold exceeded"
  }
}
```

---

### Check Workflow Status

```
GET /status/{request_id}
```

Example Response

```json
{
  "request_id": "req-1001",
  "status": "MANUAL_REVIEW"
}
```

---

### Retrieve Audit Logs

```
GET /audit/{request_id}
```

Returns a full chronological record of rule evaluations, workflow transitions, and external service interactions.

---

## Configuration Model

The system supports configuration-driven workflows and rules, allowing business logic to change without modifying source code.

### rules.json

```json
{
  "rules": [
    {
      "condition": "requested_amount > 50000",
      "action": "MANUAL_REVIEW",
      "reason": "High Risk Flag"
    },
    {
      "condition": "requested_amount <= 50000",
      "action": "APPROVED"
    }
  ]
}
```

### workflow.yaml

```yaml
max_retries: 3
retry_delay: 2
```

This design ensures flexibility and maintainability.

---

## Decision Explanation Example

Input Request

```json
{
  "request_id": "req-1001",
  "requested_amount": 60000
}
```

Rule Triggered

```
requested_amount > 50000
```

Decision

```
MANUAL_REVIEW
```

Audit Trail

```
Request Received
Rule Evaluated: requested_amount > 50000
Decision: MANUAL_REVIEW
Timestamp: 2026-03-12
```

This ensures full transparency and explainability of automated decisions.

---

## Testing Depth

The test suite validates key system behaviors.

### Happy Path
Valid request flows successfully to APPROVED status.

### Rule Branching
High-risk requests correctly route to MANUAL_REVIEW.

### Idempotency
Submitting the same request_id multiple times prevents duplicate processing.

### Dependency Failure
The workflow retries when the simulated external API fails.

### Retry Flow
Ensures retry logic triggers correctly before marking failure.

### Rule Change Scenario
Changing rule thresholds in configuration updates system behavior without code modification.

---

## Scaling Considerations

To support production-scale deployments, the system can evolve as follows:

- Replace in-memory state storage with PostgreSQL
- Introduce Redis caching for frequent lookups
- Use message queues (Kafka / RabbitMQ) for asynchronous workflow processing
- Deploy distributed worker services
- Containerize using Docker and orchestrate using Kubernetes

---

## Conclusion

This project demonstrates a robust, configurable workflow decision system capable of supporting real-world business processes.

Its modular design, configuration-driven logic, and strong fault tolerance ensure maintainability, scalability, and explainability in production environments.