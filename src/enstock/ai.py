from google import genai
from google.genai import types
from google.genai.errors import ServerError

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

prompt = """
Parse the following purchase order into CSV with exactly these columns:

SKU,UOM,QUANTITY,COST

Rules:

- QUANTITY: Only include shipped amounts. Exclude backordered or unshipped items.

- COST: Unit cost/price, not line totals.

- UOM / COST: Leave blank if not specified.

- Output raw CSV text only — include the header row, no markdown fencing, no explanation.

- Use period for decimals only (e.g., 40.50). Never use commas in numbers.

- Each row must have exactly 4 comma-separated values.

Example output:

SKU,UOM,QUANTITY,COST

1234,EACH,4,40.3

THING-1,BOX,2,59.2

NO-COST-1,,1,

"""


def _extract_text(response) -> str:
    """Extract only text parts from response, filtering out thought_signature and other non-text parts."""
    text_parts = []
    if response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text") and part.text:
                text_parts.append(part.text)
    return "".join(text_parts) if text_parts else ""


def parse_pdf(pdf: bytes) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
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
        response = _extract_text(response)
        if not response:
            response = ""
        return response
    except ServerError:
        print("Server failure, retrying..")
        return parse_pdf(pdf)
