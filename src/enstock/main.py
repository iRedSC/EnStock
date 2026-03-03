import pandas as pd
from enstock import get_purchase_order, parse_pdf, create_dataframe
from enstock.data import get_uom
from enstock.database import Database
import enstock.cli as cli
from rich import print

from enstock.db.models import BaseModel, SkuMaps, UOMs, Brands, Suppliers


# open file chooser
with cli.get_spinner() as spinner:
    spinner.add_task(description="Starting...", total=None)
    purchase_orders = get_purchase_order()

# Get database
db = Database("database.db")

BaseModel._database = db
SkuMaps.create()
UOMs.create()
Brands.create()
Suppliers.create()

# Process each file
all_output_data = []

for file_path, file_name, purchase_order_data in purchase_orders:
    # Display file name and request supplier
    print(f"\n[cyan]Processing file: {file_name}[/]")
    supplier = cli.request_supplier()
    brand = supplier.brand

    # Get current mapped SKUs for this supplier
    sku_map_data = SkuMaps.fetch_all_match_supplier(supplier)
    sku_map = {}
    for row in sku_map_data:
        sku_map[row.spn] = row.sku

    # display spinner while AI converts PDF into CSV
    with cli.get_spinner() as spinner:
        spinner.add_task(description=f"Processing {file_name}...", total=None)
        response = parse_pdf(purchase_order_data)

    # Turn CSV text into a dataframe
    df = create_dataframe(response.upper())

    # Process each row in the dataframe
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
        uom_conversion_factor = None
        if uom != None and uom.upper() != "EACH":
            uom_conversion_factor = int(get_uom(supplier, sku, uom)) # type: ignore
            amount = uom_conversion_factor * int(current_amount) # type: ignore

        all_output_data.append({
            "SKU": sku,
            "QUANTITY": amount,
            "COST": cost,
            "SHIPPING_COST": 0,
            "NOTES": "",
            "UOM_CONVERSION_FACTOR": uom_conversion_factor
        })

# Concatenate all dataframes
output_df = pd.DataFrame(all_output_data)

output_df = output_df[output_df["SKU"] != "/"]

# Create a copy for sku_cost calculation before dropping the conversion factor column
output_df_with_uom = output_df.copy()

# Group by SKU and aggregate to avoid duplicates
# COST is a unit price, so calculate weighted average based on quantity
# First, calculate total cost (unit price * quantity) for each row
output_df["TOTAL_COST"] = output_df["COST"] * output_df["QUANTITY"]

# Group and aggregate
grouped = output_df.groupby("SKU").agg({
    "QUANTITY": "sum",
    "TOTAL_COST": "sum",
    "SHIPPING_COST": "sum",
    "NOTES": lambda x: " ".join(str(v) for v in x if pd.notna(v) and str(v).strip() != "").strip() or ""
}).reset_index()

# Calculate weighted average unit price: total_cost / total_quantity
# Round to 2 decimal places
grouped["COST"] = grouped.apply(
    lambda row: round(row["TOTAL_COST"] / row["QUANTITY"], 2) if row["QUANTITY"] > 0 and pd.notna(row["TOTAL_COST"]) else None,
    axis=1
)

# Drop the temporary TOTAL_COST column and reorder columns
output_df = grouped[["SKU", "QUANTITY", "COST", "SHIPPING_COST", "NOTES"]]

# Drop UOM_CONVERSION_FACTOR from the main output (already dropped in groupby)
output_df.to_csv("output.csv", index=False)

# Create second output file with SKU and per-unit cost (per EACH)
sku_cost_data = []
for idx, row in output_df_with_uom.iterrows():
    sku = row["SKU"]
    cost = row["COST"]
    uom_conversion_factor = row.get("UOM_CONVERSION_FACTOR")
    
    # Calculate per-unit cost (per EACH)
    # If UOM was converted to EACH, divide cost by conversion factor
    # Otherwise, cost is already per EACH
    if cost is not None and cost != "":
        if uom_conversion_factor is not None and uom_conversion_factor > 0:
            # Cost was per UOM, convert to per EACH
            per_unit_cost = round(cost / uom_conversion_factor, 2)
        else:
            # Cost is already per EACH
            per_unit_cost = round(cost, 2) if pd.notna(cost) else 0
    else:
        per_unit_cost = 0
    
    sku_cost_data.append({
        "SKU": sku,
        "Cost": per_unit_cost
    })

sku_cost_df = pd.DataFrame(sku_cost_data)
# Group by SKU and average the cost in case of duplicates
sku_cost_df = sku_cost_df.groupby("SKU")["Cost"].mean().reset_index()
# Round to 2 decimal places
sku_cost_df["Cost"] = sku_cost_df["Cost"].round(2)
sku_cost_df.to_csv("sku_cost.csv", index=False)

print("[green]CSV Exported. Task Complete![/]")