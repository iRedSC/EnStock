import pandas as pd
from io import StringIO
from enstock.database import Database
from enstock.cli import request_new_uom
from enstock.models import Supplier



def create_dataframe(csv: str):
    csv_buffer = StringIO(csv)
    return pd.read_csv(csv_buffer)

def get_uom(supplier: Supplier, sku: str, uom: str, db: Database):
    amount_result = db.fetchone("SELECT amount FROM uoms WHERE supplier = ? AND sku = ? AND unit = ?", (supplier.id, sku, uom))
    if amount_result:
        amount = amount_result[0]
    else:
        amount = request_new_uom(uom, sku)
        db.execute("INSERT INTO uoms (supplier, sku, unit, amount) VALUES (?, ?, ?, ?)", (supplier.id, sku, uom, amount))
    

    return amount