from InquirerPy.resolver import prompt

completer = {
    "hello": {
        "world": None
    },
    "foo": {
        "boo": None
    },
    "fizz": {
        "bazz": None
    }
}

questions = [
    {
        "type": "input",
        "message": "FooBoo:",
        "completer": completer,
        "default": "example@email.com"
    }
]

result = prompt(questions=questions)