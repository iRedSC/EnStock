from enstock import get_purchase_order, parse_pdf, create_dataframe
from rich.progress import Progress, SpinnerColumn, TextColumn

spinner = Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),transient=True,)


purchase_order = get_purchase_order()


with spinner:
    spinner.add_task(description="Processing...", total=None)
    response = parse_pdf(purchase_order)


df = create_dataframe(response.upper())


print(df)