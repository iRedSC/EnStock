import sqlite3
from typing import Optional


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def connect(self) -> sqlite3.Connection:
        """Create and return a database connection."""
        return sqlite3.connect(self.db_path)

    def execute(
        self,
        query: str,
        params: Optional[sqlite3._Parameters] = None,
        *,
        commit: bool = True,
    ) -> None:
        """Execute a write/update/delete statement."""
        with self.connect() as conn:
            cur = conn.cursor()
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            if commit:
                conn.commit()

    def fetchall(
        self,
        query: str,
        params: Optional[sqlite3._Parameters] = None,
    ) -> list[tuple]:
        """Run a SELECT and return all rows."""
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(query, params or [])
            return cur.fetchall()

    def fetchone(
        self,
        query: str,
        params: Optional[sqlite3._Parameters] = None,
    ) -> Optional[tuple]:
        """Run a SELECT and return one row."""
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(query, params or [])
            return cur.fetchone()