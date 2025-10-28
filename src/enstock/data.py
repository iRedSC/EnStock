import pandas as pd
from io import StringIO
from enstock.cli import request_new_uom
from enstock.db.models import Supplier, UOMs



def create_dataframe(csv: str):
    csv_buffer = StringIO(csv)
    return pd.read_csv(csv_buffer)

def get_uom(supplier: Supplier, sku: str, uom: str):
    result = UOMs.fetch_uom(supplier, sku, uom)
    if result:
        amount = result.amount
    else:
        amount = request_new_uom(uom, sku)
        UOMs.insert(supplier, sku, uom, int(amount))

    return amount