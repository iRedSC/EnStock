import sqlite3
from typing import Any, Iterable, Optional
from enstock.db import uoms, sku_maps, suppliers, models

from sqlalchemy import create_engine

# create a synchronous SQLite engine
engine = create_engine("sqlite:///database.db")

connection = engine.connect()

uoms = uoms.Querier(connection)
suppliers = suppliers.Querier(connection)
sku_maps = sku_maps.Querier(connection)

def close_db():
    connection.close()