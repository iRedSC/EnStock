

from dataclasses import dataclass
from typing import Optional


@dataclass
class Brand:
    id: int
    name: str
    abbv: str

@dataclass
class Supplier:
    id: int
    name: str
    brand: Optional[Brand]