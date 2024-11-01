import json

def read_json(filename: str) -> dict:
    """ read a file and return a dict """

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except OSError as err:
        raise OSError(f"Error reading json file {filename}:", err) from err


def read_text(filename: str) -> dict:
    """ read a file and return a dict """

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()

        return data

    except OSError as err:
        raise OSError(f"Error reading text file {filename}:", err) from err
