import sqlite3
import json
import time

class AuditLogger:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._setup_db()

    def _setup_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT,
                action TEXT,
                details TEXT,
                timestamp REAL
            )
        """)
        self.conn.commit()

    def log(self, request_id: str, action: str, details: dict):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO audit_logs (request_id, action, details, timestamp)
            VALUES (?, ?, ?, ?)
        """, (request_id, action, json.dumps(details), time.time()))
        self.conn.commit()

    def get_logs(self, request_id: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT action, details, timestamp FROM audit_logs WHERE request_id = ?", (request_id,))
        return [{"action": r[0], "details": json.loads(r[1]), "timestamp": r[2]} for r in cursor.fetchall()]