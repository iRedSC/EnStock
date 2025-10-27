-- name: GetSkuMapBySupplier :many
SELECT spn, sku FROM sku_maps WHERE supplier = :supplier;

-- name: InsertSkuMap :exec
INSERT INTO sku_maps (supplier, spn, sku)
VALUES (:supplier, :spn, :sku);