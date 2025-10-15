from google import genai
from google.genai import types

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

prompt = "Convert the following purchase order into a csv with these columns, and answer only with the raw text: SKU, UOM (EACH if not present), QUANTITY, COST"

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
    )
    response = response.text
    if not response:
        response = ""
    return response