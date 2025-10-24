-- name: GetSkuMapBySupplier :many
SELECT spn, sku FROM sku_maps WHERE supplier = ?;

-- name: InsertSkuMap :exec
INSERT INTO sku_maps (supplier, spn, sku)
VALUES (?, ?, ?);