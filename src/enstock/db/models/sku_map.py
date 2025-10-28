from dataclasses import dataclass
from enstock.db.models.base_model import BaseModel
from enstock.db.models.supplier import Supplier


CREATE_TABLE = \
"""
CREATE TABLE IF NOT EXISTS sku_maps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier INTEGER NOT NULL,
    spn TEXT NOT NULL,
    sku TEXT NOT NULL,
    FOREIGN KEY (supplier) REFERENCES suppliers(id),
    UNIQUE (supplier, spn)
);
"""

@dataclass
class SkuMap:
    id: int
    supplier: int
    spn: str
    sku: str

class SkuMaps(BaseModel):
    _create_table_statement = CREATE_TABLE


    @classmethod
    def fetch_all_match_supplier(cls, supplier: Supplier) -> list[SkuMap]:
        rows = cls.database().fetchall("SELECT * FROM sku_maps WHERE supplier = ?", (supplier.id,))
        results = []
        for row in rows:
            results.append(SkuMap(row[0], row[1], row[2], row[3]))
        return results

    @classmethod
    def insert(cls, supplier: Supplier, spn: str, sku: str):
        row = cls.database().fetchone("INSERT INTO sku_maps (supplier, spn, sku) VALUES (?, ?, ?) RETURNING *", (supplier.id, spn, sku))
        return SkuMap(row[0], row[1], row[2], row[3]) # type: ignore

