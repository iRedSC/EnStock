-- name: GetUOMAmount :one
SELECT amount FROM uoms
WHERE supplier = ? AND sku = ? AND unit = ?;

-- name: InsertUOM :exec
INSERT INTO uoms (supplier, sku, unit, amount)
VALUES (?, ?, ?, ?);