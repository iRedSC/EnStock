from enstock import get_purchase_order, parse_pdf, create_dataframe
from enstock.data import get_uom
from enstock.database import Database, init_db
import enstock.cli as cli


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
init_db(db)

# User provides supplier
supplier = cli.request_supplier(db)
brand = supplier.brand

# Get current mapped SKUs
sku_map_data = db.fetchall("SELECT * FROM sku_maps WHERE supplier = ?", (supplier.id,))
sku_map = {}
for row in sku_map_data:
    sku_map[row[1]] = row[2]

print(df)

for idx, row in df.iterrows():
    uom = row.get("UOM")
    spn = row.get("SKU")
    current_amount = row.get("QUANTITY")
    if not spn:
        continue
    if spn not in sku_map:
        sku = cli.map_sku(spn, brand)
        sku_map[spn] = sku
    else:
        sku = sku_map.get(spn)
    
    if uom != None and uom.upper() != "EACH":
        amount = get_uom(supplier, uom, db)
        df.at[idx, "QUANTITY"] = int(amount) * int(current_amount) # type: ignore

    db.execute("INSERT INTO sku_maps (supplier, spn, sku) VALUES (?, ?, ?)", (supplier.id, spn, sku))

df["SKU"] = df["SKU"].map(sku_map).fillna(df["SKU"])
df = df[df["SKU"] != "/"]

print(df)

df.to_csv("output.csv", index=False)