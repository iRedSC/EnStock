from dataclasses import dataclass
from enstock.db.models.base_model import BaseModel
from enstock.db.models.brand import Brand


CREATE_TABLE = \
"""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL,
    brand INTEGER NOT NULL,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    barcode TEXT NOT NULL,
    FOREIGN KEY (brand) REFERENCES brands(id),
    UNIQUE (sku)
);
"""

FETCH_ALL_MATCH_BRAND = \
"""
SELECT p.id, p.sku, p.name, p.price, p.barcode,
        b.id AS brand_id, b.name AS brand_name, b.abbv AS brand_abbv
FROM products p
JOIN brands b ON p.supplier = b.id
WHERE b.id = ?
"""

@dataclass
class Product:
    id: int
    sku: str
    name: str
    price: int
    barcode: str
    brand: Brand

class Products(BaseModel):
    _create_table_statement = CREATE_TABLE


    @classmethod
    def fetch_all_match_brand(cls, brand: Brand) -> dict[str, Product]:
        rows = cls.database().fetchall(FETCH_ALL_MATCH_BRAND, (brand.id,))
        results = dict()
        for row in rows:
            results[row[1]] = Product(row[0], row[1], row[2], row[3], row[4], Brand(row[5], row[6], row[7]))
        return results

    @classmethod
    def insert(cls, sku: str, name: str, price: int, barcode: str, brand: Brand):
        row = cls.database().fetchone("INSERT INTO sku_maps (sku, name, price, barcode, brand) VALUES (?, ?, ?) RETURNING *", (sku, name, price, barcode, brand.id))
        return Product(row[0], row[1], row[2], row[3], row[4], brand) # type: ignore

