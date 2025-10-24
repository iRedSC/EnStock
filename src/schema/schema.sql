-- brands table
CREATE TABLE brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    abbv TEXT NOT NULL
);

-- suppliers table
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand INTEGER,
    FOREIGN KEY (brand) REFERENCES brands(id)
);

-- sku_maps table
CREATE TABLE sku_maps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier INTEGER NOT NULL,
    spn TEXT NOT NULL,
    sku TEXT NOT NULL,
    FOREIGN KEY (supplier) REFERENCES suppliers(id),
    UNIQUE (supplier, spn)
);

-- uoms table
CREATE TABLE uoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier INTEGER NOT NULL,
    sku TEXT NOT NULL,
    unit TEXT NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (supplier) REFERENCES suppliers(id)
);