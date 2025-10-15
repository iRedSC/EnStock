from enstock import get_purchase_order, parse_pdf, create_dataframe
from rich.progress import Progress, SpinnerColumn, TextColumn
import enstock.user_input as user

spinner = Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),transient=True,)

# open file chooser
purchase_order = get_purchase_order()

# display spinner while AI converts PDF into CSV
with spinner:
    spinner.add_task(description="Processing...", total=None)
    response = parse_pdf(purchase_order)

# Turn CSV text into a dataframe
df = create_dataframe(response.upper())


sku_map = {}

for idx, row in df.iterrows():
    spn = row["SKU"]
    if spn not in sku_map:
        sku = user.map_sku(spn)
        sku_map[spn] = sku

print(df)