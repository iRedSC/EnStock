from typing import Literal
from InquirerPy.resolver import prompt
from InquirerPy.base.control import Choice
from rich.progress import Progress, SpinnerColumn, TextColumn
from enstock.data import Brand, Supplier
from enstock.database import Database


def get_spinner():
    return Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),transient=True,)

def map_sku(sku: str, brand: Brand | None):
    prefix = ""
    if brand:
        prefix = f"{brand.abbv}-"
    questions = [
        {
            "type": "input",
            "message": f"Enter mapped SKU for SPN <{sku}> (default: {prefix}{sku.upper()}):",
            "transformer": lambda result: result.upper() or f"{prefix}{sku.upper()}"
        }
    ]
    result = prompt(questions=questions,style_override=False, style={"answermark": "green", "answered_question": "#66ffe3"})[0]
    if result == '':
        result = f"{prefix}{sku.upper()}"
    elif type(result) == str:
        result = result.upper()
    return result


def request_new_brand(abbv: str):
    new_brand = [
        {
            "name": "name",
            "type": "input",
            "message": "Brand name for new brand:",
            "mandatory": True
        }, 
        {
            "name": "abbv",
            "type": "input",
            "message": "Brand abbreviation:",
            "default": abbv,
            "mandatory": True,
        }
    ]
    result: dict[Literal["name", "abbv"], str] = prompt(questions=new_brand, style_override=False, style={"answermark": "green", "answered_question": "#66ffe3"}) # type: ignore
    return result

def request_supplier(db: Database) -> Supplier:
    suppliers: list[tuple[int, str, str, str]] = db.fetchall("""
SELECT
    suppliers.id,
    suppliers.name AS supplier_name,
    brands.name AS brand_name,
    brands.abbv AS brand_abbv
FROM suppliers
LEFT JOIN brands ON suppliers.brand = brands.id
                            """)

    choose_supplier = {
        "name": "choose_supplier",
        "type": "list",
        "message": "Choose a supplier:",
        "choices": [*[Choice(value=Supplier(supplier[1], Brand(supplier[2], supplier[3]) if supplier[2] else None), name=supplier[1]) for supplier in suppliers], Choice(value={"error": True}, name="* New")],
        "default": {"error": True},
    }



    supplier: dict = prompt(questions=choose_supplier, style_override=False, style={"answermark": "green", "answered_question": "#66ffe3"}).get("choose_supplier") # type: ignore
    if supplier.get("name"):
        return Supplier(supplier["name"], supplier["brand"])
    

    new_supplier = [
        {
            "name": "supplier_name",
            "type": "input",
            "message": "Supplier name:",
            "mandatory": True
        }, 
        {
            "name": "brand_abbv",
            "type": "input",
            "message": "Brand abbreviation for supplier (enter to skip)",
        }
    ]

    result = prompt(questions=new_supplier, style_override=False, style={"answermark": "green", "answered_question": "#66ffe3"})
    supplier_name: str = result.get("supplier_name") # type: ignore
    brand_abbv = result.get("brand_abbv")

    if type(brand_abbv) == str and brand_abbv != "":
        brand_info: tuple[int, str, str] | None = db.fetchone("SELECT * FROM brands WHERE abbv = ?", (brand_abbv,))

        if not brand_info:
            result = request_new_brand(brand_abbv)
            brand = Brand(result["name"], result["abbv"])
            db.execute("INSERT INTO brands (name, abbv) VALUES (?, ?)", (result["name"], result["abbv"]))
            brand_info = (0, brand.name, brand.abbv)

        brand = Brand(brand_info[1], brand_info[2])
        db.execute("INSERT INTO suppliers (name, brand) VALUES (?, ?)", (supplier_name, brand_info[0]))
        return Supplier(supplier_name, brand)
    
    db.execute("INSERT INTO suppliers (name, brand) VALUES (?, ?)", (supplier_name, None))
    return Supplier(supplier_name, None)
