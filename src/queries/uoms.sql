-- name: GetUOMAmount :one
SELECT amount FROM uoms
WHERE supplier = :supplier AND sku = :sku AND unit = :unit;

-- name: InsertUOM :exec
INSERT INTO uoms (supplier, sku, unit, amount)
VALUES (:supplier, :sku, :unit, :amount);