from google import genai
from google.genai import types

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

prompt = """
Convert the following purchase order into a csv.

Answer only with the raw text, make sure to include exact headers.

Supply these columns, and use headers in your output: SKU, UOM, QUANTITY, COST

If UOM or COST is not specified, leave blank. Don't wrap in ```csv``` as that will break the system.

Make sure to include CSV header titles in your output, as not doing so will break the system.

Output Example:

SKU,UOM,QUANTITY,COST
1234,EACH,4,40.3
THING-1,BOX,2,59.2
NO-COST-1,,1,

"""
def parse_pdf(pdf: bytes) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=pdf,
                mime_type="application/pdf",
            ),
            prompt,
        ],
        config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
    ),
    )
    response = response.text
    if not response:
        response = ""
    return response