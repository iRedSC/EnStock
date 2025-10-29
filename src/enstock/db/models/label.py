from dataclasses import dataclass
from enstock.db.models.base_model import BaseModel


CREATE_TABLE = \
"""
CREATE TABLE IF NOT EXISTS labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    abbv TEXT NOT NULL
);
"""

@dataclass
class Label:
    id: int
    sku: str
    name_en: str
    name_es: str
    price: int
    barcode: str
    brand: str

class Brands(BaseModel):
    _create_table_statement = CREATE_TABLE