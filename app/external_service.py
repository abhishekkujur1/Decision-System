import random
import time

class ExternalVerificationService:
    @staticmethod
    def verify_document(document_id: str) -> bool:
        # Simulate network delay
        time.sleep(0.5)
        # Simulate 30% failure rate for retry logic demonstration
        if random.random() < 0.3:
            raise ConnectionError("External API dependency failed. Timeout.")
        return True