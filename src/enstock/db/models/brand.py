from dataclasses import dataclass
from enstock.db.models.base_model import BaseModel


CREATE_TABLE = \
"""
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    abbv TEXT NOT NULL
);
"""

@dataclass
class Brand:
    id: int
    name: str
    abbv: str

class Brands(BaseModel):
    _create_table_statement = CREATE_TABLE


    @classmethod
    def fetch_matching_abbv(cls, abbv: str) -> Brand | None:
        row = cls.database().fetchone("SELECT * FROM brands WHERE abbv = ?", (abbv,))
        if row:
            return Brand(row[0], row[1], row[2])
        return

    @classmethod
    def insert(cls, name: str, abbv: str):
        row = cls.database().fetchone("INSERT INTO brands (name, abbv) VALUES (?, ?) RETURNING *", (name, abbv))
        return Brand(row[0], row[1], row[2]) # type: ignore