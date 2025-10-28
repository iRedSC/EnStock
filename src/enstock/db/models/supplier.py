from dataclasses import dataclass
from typing import Optional
from enstock.db.models.base_model import BaseModel
from enstock.db.models.brand import Brand


CREATE_TABLE = \
"""
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand INTEGER,
    FOREIGN KEY (brand) REFERENCES brands(id)
);
"""

FETCH_ALL = \
"""
SELECT
    suppliers.id,
    suppliers.name AS supplier_name,
    brands.id AS brand_id,
    brands.name AS brand_name,
    brands.abbv AS brand_abbv
FROM suppliers
LEFT JOIN brands ON suppliers.brand = brands.id
"""

@dataclass
class Supplier:
    id: int
    name: str
    brand: Optional[Brand]

class Suppliers(BaseModel):
    _create_table_statement = CREATE_TABLE


    @classmethod
    def fetch_all(cls) -> list[Supplier]:
        rows = cls.database().fetchall(FETCH_ALL)
        results = []
        for row in rows:
            results.append(Supplier(row[0], row[1], Brand(row[2], row[3], row[4])))
        return results

    @classmethod
    def insert(cls, name: str, brand: Optional[Brand]):
        row = cls.database().fetchone("INSERT INTO suppliers (name, brand) VALUES (?, ?) RETURNING *", (name, brand.id if brand else None))
        return Supplier(row[0], row[1], row[2]) # type: ignore