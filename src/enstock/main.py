import pandas as pd
from enstock import get_purchase_order, parse_pdf, create_dataframe
from enstock.data import get_uom
from enstock.database import Database
import enstock.cli as cli
from rich import print

from enstock.db.models.base_model import BaseModel
from enstock.db.models.sku_map import SkuMaps
from enstock.db.models.uom import UOMs


# open file chooser
with cli.get_spinner() as spinner:
    spinner.add_task(description="Starting...", total=None)
    purchase_order = get_purchase_order()


# display spinner while AI converts PDF into CSV
with cli.get_spinner() as spinner:
    spinner.add_task(description="Processing...", total=None)
    response = parse_pdf(purchase_order)

# Turn CSV text into a dataframe
df = create_dataframe(response.upper())

# Get database
db = Database("database.db")

BaseModel._database = db
SkuMaps.create()
UOMs.create()


# User provides supplier
supplier = cli.request_supplier()
brand = supplier.brand

# Get current mapped SKUs
sku_map_data = SkuMaps.fetch_all_match_supplier(supplier)
sku_map = {}
for row in sku_map_data:
    sku_map[row.spn] = row.sku

output_data = []


for idx, row in df.iterrows():
    uom = row.get("UOM")
    spn = row.get("SKU")
    current_amount = row.get("QUANTITY")
    cost = row.get("COST")

    if not spn:
        continue
    if spn not in sku_map:
        sku = cli.map_sku(spn, brand)
        sku_map[spn] = sku
        SkuMaps.insert(supplier, spn, sku)
    else:
        sku: str = sku_map[spn]
    
    if type(uom) == float:
        uom = None

    amount = current_amount
    if uom != None and uom.upper() != "EACH":
        amount = int(get_uom(supplier, sku, uom)) * int(current_amount) # type: ignore

    output_data.append({
        "SKU": sku,
        "QUANTITY": amount,
        "COST": cost,
        "SHIPPING_COST": 0,
        "NOTES": ""
    })
    
        
close_db()
output_df = pd.DataFrame(output_data)

output_df = output_df[output_df["SKU"] != "/"]


output_df.to_csv("output.csv", index=False)

print("[green]CSV Exported. Task Complete![/]")