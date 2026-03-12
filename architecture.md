# Architecture & Design Document

## 1. System Components

### API Layer (FastAPI)
Acts as the entry point for the system. It accepts incoming requests, validates the schema, and forwards valid requests to the workflow engine for processing.

### Workflow Engine
The central orchestrator responsible for executing workflow stages. It manages the request lifecycle, handles retries for failed operations, and coordinates interactions between the rule engine, state manager, and external services.

### Rule Engine
A stateless component responsible for evaluating business rules defined in external configuration (`rules.json`).  
It processes request data against configured conditions to determine workflow outcomes such as approval, rejection, or manual review.

### State Manager
Maintains the lifecycle state of each request and ensures idempotency.  
It prevents duplicate processing of the same `request_id` and records the current status of each workflow instance.

### Audit Logger
Captures a detailed audit trail of system activity.  
It records:

- request inputs
- rules triggered
- decisions made
- timestamps of workflow events

This enables full explainability and traceability of automated decisions.

### External Service Simulator
Simulates a fragile external dependency (e.g., a credit scoring API).  
This component is used to test system resilience by introducing occasional failures and validating retry mechanisms.

---

## 2. Data Flow & Execution

The request lifecycle follows these steps:

1. **Request Intake**
   - The API receives the request.
   - Input schema is validated.
   - The State Manager checks for idempotency using `request_id`.

2. **External Dependency Interaction**
   - The Workflow Engine calls the simulated external service.
   - If the call fails, retry logic is applied based on configuration in `workflow.yaml`.

3. **Rule Evaluation**
   - The Rule Engine evaluates business rules defined in `rules.json`.
   - Rules may include threshold checks, mandatory validations, or conditional branching.

4. **Decision Finalization**
   - A final decision is determined:
     - APPROVED
     - REJECTED
     - MANUAL_REVIEW
   - The State Manager updates the workflow status.
   - The Audit Logger records the full execution trace.

---

## 3. Design Trade-offs

### SQLite for State Storage
SQLite was chosen to provide persistence with minimal setup.  
It supports ACID compliance and allows the system to run immediately without requiring a database server.

### Synchronous Workflow Processing
The system uses synchronous execution for simplicity and reliability within the hackathon scope.  
However, the modular architecture allows easy migration to asynchronous background workers if required.

### Configuration-Driven Rules
Business rules are defined in external configuration files (`JSON/YAML`).  
This ensures workflows can evolve without requiring changes to application code.

### Modular System Design
Each major function (API, workflow engine, rule engine, state manager, audit logger) is implemented as a separate module to reduce coupling and improve maintainability.

---

## 4. Scaling Considerations

To support large-scale deployments, the system can evolve in the following ways:

### Distributed Workers
Workflow execution can be moved to background workers using tools such as:

- Celery
- RabbitMQ
- Kafka

This enables horizontal scaling for high request throughput.

### Database Migration
SQLite can be replaced with a production-grade database such as:

- PostgreSQL
- MySQL

This would support concurrent processing and distributed systems.

### Containerization
Docker containers can be used to package the application and ensure consistent deployment environments.

### Caching Layer
Redis can be introduced to cache rule configurations and frequently accessed workflow states, reducing latency.

---

## 5. Decision Explainability

Every decision produced by the system is fully explainable through the audit trail.

Each audit entry includes:

- Original input request data
- Rules evaluated during processing
- Rules that triggered the decision
- Final workflow outcome
- Timestamp for each lifecycle event

Example explanation:

Input:
```
requested_amount = 60000
```

Rule Triggered:
```
requested_amount > 50000
```

Decision:
```
MANUAL_REVIEW
```

Audit Trace:
```
Request Received
Rule Evaluated: requested_amount > 50000
Decision: MANUAL_REVIEW
Timestamp: 2026-03-12
```

This approach ensures transparency and accountability for automated decision-making systems.