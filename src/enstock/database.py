import sqlite3
from typing import Any, Iterable, Optional


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

def init_db(db: Database):
    db.execute("""
    CREATE TABLE IF NOT EXISTS brands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        abbv TEXT NOT NULL
    );
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        brand INTEGER,
        FOREIGN KEY (brand) REFERENCES brands(id)
    );
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS sku_maps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier INTEGER NOT NULL,
        spn TEXT NOT NULL,
        sku TEXT NOT NULL,
        FOREIGN KEY (supplier) REFERENCES suppliers(id),
        UNIQUE (supplier, spn)
    );
               """)
               
    db.execute("""
    CREATE TABLE IF NOT EXISTS uoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier INTEGER NOT NULL,
    sku TEXT NOT NULL,
    unit TEXT NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (supplier) REFERENCES suppliers(id)
    );
               """)