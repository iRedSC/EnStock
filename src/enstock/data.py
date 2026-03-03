import re
import pandas as pd
from io import StringIO
from enstock.cli import request_new_uom
from enstock.db.models import Supplier, UOMs


def _sanitize_csv(csv: str) -> str:
    """Strip markdown code blocks and normalize line endings."""
    csv = csv.strip()
    # Remove markdown code blocks (```csv ... ``` or ``` ... ```)
    csv = re.sub(r"^```(?:csv)?\s*\n?", "", csv)
    csv = re.sub(r"\n?```\s*$", "", csv)
    csv = csv.strip()
    # Normalize line endings and trim each line
    lines = [line.strip() for line in csv.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    return "\n".join(lines)


def create_dataframe(csv: str):
    csv = _sanitize_csv(csv)
    csv_buffer = StringIO(csv)
    return pd.read_csv(csv_buffer, on_bad_lines="warn")


def get_uom(supplier: Supplier, sku: str, uom: str):
    result = UOMs.fetch_uom(supplier, sku, uom)
    if result:
        amount = result.amount
    else:
        amount = request_new_uom(uom, sku)
        UOMs.insert(supplier, sku, uom, int(amount))

    return amount