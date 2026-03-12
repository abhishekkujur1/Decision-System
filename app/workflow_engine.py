import yaml
from .state_manager import StateManager
from .audit_logger import AuditLogger
from .rule_engine import RuleEngine
from .external_service import ExternalVerificationService

class WorkflowEngine:
    def __init__(self, state_mgr: StateManager, audit_mgr: AuditLogger):
        self.state = state_mgr
        self.audit = audit_mgr
        self.rules = RuleEngine()
        
        with open("config/workflow.yaml", 'r') as f:
            self.config = yaml.safe_load(f)

    def process(self, request_id: str, workflow_type: str, data: dict):
        if self.state.is_duplicate(request_id):
            return {"message": "Idempotent request. Already processed."}

        self.state.save_state(request_id, "PROCESSING", data)
        self.audit.log(request_id, "STARTED", {"workflow": workflow_type})

        # Stage 1: External Dependency with Retry
        max_retries = self.config.get("global_settings", {}).get("max_retries", 3)
        external_success = False
        
        for attempt in range(max_retries):
            try:
                ExternalVerificationService.verify_document(data.get("doc_id", "default"))
                external_success = True
                self.audit.log(request_id, "EXTERNAL_CHECK_PASSED", {"attempt": attempt + 1})
                break
            except Exception as e:
                self.audit.log(request_id, "EXTERNAL_CHECK_FAILED", {"attempt": attempt + 1, "error": str(e)})
        
        if not external_success:
            self.state.save_state(request_id, "FAILED", data)
            return {"status": "FAILED", "reason": "External dependency unavailable"}

        # Stage 2: Rule Evaluation
        decision = self.rules.evaluate(workflow_type, data)
        self.audit.log(request_id, "RULES_EVALUATED", decision)

        # Stage 3: Finalize State
        final_status = decision["status"]
        self.state.save_state(request_id, final_status, data)
        self.audit.log(request_id, "COMPLETED", {"final_status": final_status})

        return {"request_id": request_id, "status": final_status, "decision": decision}