import sqlite3
import json

class StateManager:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._setup_db()

    def _setup_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                request_id TEXT PRIMARY KEY,
                status TEXT,
                data TEXT
            )
        """)
        self.conn.commit()

    def is_duplicate(self, request_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM requests WHERE request_id = ?", (request_id,))
        return cursor.fetchone() is not None

    def save_state(self, request_id: str, status: str, data: dict):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO requests (request_id, status, data) 
            VALUES (?, ?, ?)
            ON CONFLICT(request_id) DO UPDATE SET status=excluded.status, data=excluded.data
        """, (request_id, status, json.dumps(data)))
        self.conn.commit()

    def get_state(self, request_id: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT status, data FROM requests WHERE request_id = ?", (request_id,))
        row = cursor.fetchone()
        if row:
            return {"request_id": request_id, "status": row[0], "data": json.loads(row[1])}
        return None