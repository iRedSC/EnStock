PRAGMA foreign_keys = ON;

CREATE TABLE brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    abbv TEXT NOT NULL
);

CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_id INTEGER REFERENCES brands(id) ON DELETE SET NULL,
    sku TEXT NOT NULL,
    name TEXT NOT NULL,
    cost INTEGER NOT NULL,
    price INTEGER NOT NULL,
    weight REAL,
    height REAL,
    width REAL,
    depth REAL,
    FOREIGN KEY (brand_id) REFERENCES brands(id)
);

CREATE TABLE uoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    uom TEXT NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE
);

CREATE TABLE sku_maps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spn TEXT NOT NULL,
    sku  TEXT NOT NULL,
)