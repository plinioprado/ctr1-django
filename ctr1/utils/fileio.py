""" Utilities - file - csv """

import json
import csv


def read_text(filename: str) -> str:
    """ read a file and return a dict """

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()

        return data

    except OSError as err:
        raise OSError(f"Error reading text file {filename}:", err) from err


def write_text(filename: str, txt: str) -> None:
    """ read a file and return a dict """

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"{txt}\n")

            return None

    except OSError as err:
        raise OSError(f"Error writing to file {filename}:", err) from err


def add_text(filename: str, txt: str) -> None:
    """ read a file and return a dict """

    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"{txt}\n")

            return None

    except OSError as err:
        raise OSError(f"Error writing to file {filename}:", err) from err

def read_json(filename: str) -> dict:
    """ read a file and return a dict """

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except OSError as err:
        raise OSError(f"Error reading json file {filename}:", err) from err


def write_csv(filename: str, rows: list) -> None:
    """ Save the report as csv file """

    try:

        with open(filename, "w", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            for row in rows:
                writer.writerow(row)

    except OSError as err:
        raise OSError(f"Error writing csv file {filename}:", err) from err


def read_csv(filename: str) -> list[dict]:
    """ Save the report as csv file """

    try:

        with open(filename, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

        return rows

    except OSError as err:
        raise OSError(f"Error reading csv file {filename}:", err) from err


def get_file_settings() -> dict:
    settings = read_json("./ctr1/settings.json")

    return settings
