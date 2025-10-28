from dataclasses import dataclass
from enstock.db.models.base_model import BaseModel
from enstock.db.models.supplier import Supplier


CREATE_TABLE = \
"""
CREATE TABLE IF NOT EXISTS uoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier INTEGER NOT NULL,
    sku TEXT NOT NULL,
    unit TEXT NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (supplier) REFERENCES suppliers(id)
);
"""

@dataclass
class UOM:
    id: int
    supplier: int
    sku: str
    unit: str
    amount: int

class UOMs(BaseModel):
    _create_table_statement = CREATE_TABLE


    @classmethod
    def fetch_uom(cls, supplier: Supplier, sku: str, uom: str) -> UOM | None:
        row = cls.database().fetchone("SELECT * FROM uoms WHERE supplier = ? AND sku = ? AND unit = ?", (supplier.id, sku, uom))
        if not row:
            return
        return UOM(row[0], row[1], row[2], row[3], row[4])

    @classmethod
    def insert(cls, supplier: Supplier, sku: str, uom: str, amount: int):
        row = cls.database().fetchone("INSERT INTO uoms (supplier, sku, unit, amount) VALUES (?, ?, ?, ?) RETURNING *", (supplier.id, sku, uom, amount))
        return UOM(row[0], row[1], row[2], row[3], row[4]) #type: ignore

