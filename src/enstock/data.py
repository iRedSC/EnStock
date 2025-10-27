import pandas as pd
from io import StringIO
from enstock.database import uoms
from enstock.cli import request_new_uom
from enstock.db.models import Supplier


def create_dataframe(csv: str):
    csv_buffer = StringIO(csv)
    return pd.read_csv(csv_buffer)

def get_uom(supplier: Supplier, sku: str, uom: str):
    amount_result = uoms.get_uom_amount(supplier=supplier.id, sku=sku, unit=uom)
    if amount_result:
        amount = amount_result[0]
    else:
        amount = request_new_uom(uom, sku)
        uoms.insert_uom(supplier=supplier.id, sku=sku, unit=uom, amount=amount)
    
    return amount