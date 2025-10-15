from InquirerPy.resolver import prompt
from termcolor import colored


def map_sku(sku: str):
    questions = [
        {
            "type": "input",
            "message": f"Enter SKU [{sku.upper()}]:",
            "transformer": lambda result: result.upper() or sku.upper()
        }
    ]
    return prompt(questions=questions)

