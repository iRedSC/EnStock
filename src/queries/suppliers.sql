-- name: GetSuppliersWithBrand :many
SELECT
    suppliers.id,
    suppliers.name AS supplier_name,
    brands.id AS brand_id,
    brands.name AS brand_name,
    brands.abbv AS brand_abbv
FROM suppliers
LEFT JOIN brands ON suppliers.brand = brands.id;

-- name: GetBrandByAbbv :one
SELECT * FROM brands WHERE abbv = ?;

-- name: InsertBrand :one
INSERT INTO brands (name, abbv)
VALUES (?, ?)
RETURNING id;

-- name: InsertSupplierWithBrand :one
INSERT INTO suppliers (name, brand)
VALUES (?, ?)
RETURNING id;

-- name: InsertSupplierNoBrand :one
INSERT INTO suppliers (name, brand)
VALUES (?, NULL)
RETURNING id;