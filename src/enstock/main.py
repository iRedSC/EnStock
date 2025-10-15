from google import genai
from google.genai import types
from enstock.dialog import get_purchase_order
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

purchase_order = get_purchase_order()


prompt = "Convert the following purchase order into a csv with these columns, and answer only with the raw text: SKU, UOM (EACH if not present), QUANTITY, COST"




with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
    progress.add_task(description="Processing...", total=None)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=purchase_order,
                mime_type="application/pdf",
            ),
            prompt,
        ],
    )

print("\n--- Response ---\n")
print(response.text)