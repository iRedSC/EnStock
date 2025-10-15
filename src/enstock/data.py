import pandas as pd
from io import StringIO

def create_dataframe(csv: str):
    csv_buffer = StringIO(csv)
    return pd.read_csv(csv_buffer)