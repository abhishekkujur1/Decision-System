import json

class RuleEngine:
    def __init__(self, config_path="config/rules.json"):
        with open(config_path, 'r') as f:
            self.rules = json.load(f)

    def evaluate(self, workflow_type: str, data: dict) -> dict:
        if workflow_type not in self.rules:
            return {"status": "REJECTED", "reason": "No rules defined for workflow"}

        workflow_rules = self.rules[workflow_type]
        triggered_rules = []

        # Threshold checks
        for rule in workflow_rules.get("thresholds", []):
            field = rule["field"]
            operator = rule["operator"]
            value = rule["value"]
            
            if field in data:
                if operator == ">" and data[field] > value:
                    triggered_rules.append(rule["name"])
                elif operator == "<" and data[field] < value:
                    triggered_rules.append(rule["name"])

        # Conditional branching based on triggers
        if "High Risk Flag" in triggered_rules:
            return {"status": "MANUAL_REVIEW", "triggered": triggered_rules, "reason": "Risk threshold exceeded"}
            
        return {"status": "APPROVED", "triggered": triggered_rules, "reason": "All checks passed"}