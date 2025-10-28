from typing import Literal
from InquirerPy.resolver import prompt
from InquirerPy.base.control import Choice
from rich.progress import Progress, SpinnerColumn, TextColumn
from enstock.db.models import Supplier, Brand, Brands, Suppliers


def get_spinner():
    return Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),transient=True,)

def map_sku(sku: str, brand: Brand | None) -> str:
    formatted_sku = sku.upper().split()[0]
    prefix = ""
    if brand:
        prefix = f"{brand.abbv}-"
    questions = [
        {
            "type": "input",
            "message": f"Enter mapped SKU for SPN <{sku}> (default: {prefix}{formatted_sku}):",
            "transformer": lambda result: result.upper() or f"{prefix}{formatted_sku}"
        }
    ]
    result = prompt(questions=questions,style_override=False, style={"answermark": "green", "answered_question": "#66ffe3"})[0]
    if result == '':
        result = f"{prefix}{formatted_sku}"
    elif type(result) == str:
        result = result.upper()
    return result # type: ignore


def request_new_uom(uom: str, sku: str) -> str:
    new_uom = [
        {
            "name": "uom_amount",
            "type": "number",
            "message": f"How many of EACH in {uom} of {sku}?",
            "min_allowed": 1,
            "validate": lambda result: len(result) > 0,
            "invalid_message": "Please enter a number.",
            "default": None,
        }
    ]

    result = prompt(questions=new_uom, style_override=False, style={"answermark": "green", "answered_question": "#66ffe3"})
    amount = result.get("uom_amount")
    return amount # type: ignore



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


def request_new_supplier():
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
    return (supplier_name, brand_abbv)

def request_supplier() -> Supplier:
    suppliers: list[Supplier] = Suppliers.fetch_all()
    choose_supplier = {
        "name": "choose_supplier",
        "type": "list",
        "message": "Choose a supplier:",
        "choices": [*[Choice(value=supplier, name=supplier.name) for supplier in suppliers], Choice(value={"error": True}, name="* New")],
        "default": {"error": True},
    }



    supplier: dict = prompt(questions=choose_supplier, style_override=False, style={"answermark": "green", "answered_question": "#66ffe3"}).get("choose_supplier") # type: ignore
    if supplier.get("name"):
        if supplier["brand"]:
            return Supplier(supplier["id"], supplier["name"], Brand(supplier["brand"]["id"], supplier["brand"]["name"], supplier["brand"]["abbv"]))
        return Supplier(supplier["id"], supplier["name"], None)
    

    supplier_name, brand_abbv = request_new_supplier()

    if type(brand_abbv) == str and brand_abbv != "":
        brand: Brand | None = Brands.fetch_matching_abbv(brand_abbv)

        if not brand:
            result = request_new_brand(brand_abbv)
            brand = Brands.insert(result["name"], result["abbv"])

        return Suppliers.insert(supplier_name, brand)

    return Suppliers.insert(supplier_name, None)

