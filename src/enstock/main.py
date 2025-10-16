from enstock import get_purchase_order, parse_pdf, create_dataframe
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
sku_map_data = db.fetchall("SELECT * FROM sku_maps")
sku_map = {}
for row in sku_map_data:
    sku_map[row[1]] = row[2]


print(df)

for idx, row in df.iterrows():
    spn = row.get("SKU")
    if not spn:
        continue
    if spn not in sku_map:
        sku = cli.map_sku(spn, brand)
        sku_map[spn] = sku
        db.execute("INSERT INTO sku_maps (spn, sku) VALUES (?, ?)", (spn, sku))

df["SKU"] = df["SKU"].map(sku_map).fillna(df["SKU"])
df = df[df["SKU"] != "/"]

print(df)