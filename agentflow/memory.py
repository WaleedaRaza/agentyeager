import sqlite3
from typing import Optional
import json

class Memory:
    def __init__(self, db_path: str = "agentflow_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)")
        self.conn.commit()

    def store(self, key: str, value: str):
        self.cursor.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def retrieve(self, key: str) -> Optional[str]:
        self.cursor.execute("SELECT value FROM memory WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def store_json(self, key: str, value: dict):
        """Store a dictionary as JSON."""
        self.store(key, json.dumps(value))

    def retrieve_json(self, key: str) -> Optional[dict]:
        """Retrieve and parse JSON data."""
        value = self.retrieve(key)
        return json.loads(value) if value else None