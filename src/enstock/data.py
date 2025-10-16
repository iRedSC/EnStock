from dataclasses import dataclass
import pandas as pd
from io import StringIO
from typing import Optional

@dataclass
class Brand:
    name: str
    abbv: str

@dataclass
class Supplier:
    name: str
    brand: Optional[Brand]

def create_dataframe(csv: str):
    csv_buffer = StringIO(csv)
    return pd.read_csv(csv_buffer)