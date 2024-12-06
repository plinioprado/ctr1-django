"""
crud generic sqlite tables returning Python lists or dictionaries

"""

import csv
import sqlite3
from ledger1.utils import dbutil


def get_many(table_name: str):
    print(f"will select from {table_name}")

    return []


def get_one(table_name: str, aux_id: int):
    print(f"will select {aux_id} from {table_name}")

    return {}



def restore(table_name: str, file_name: str)-> None:
    """ Restore from CSV """

    con, cur = dbutil.get_connection()

    try:

        with open(file_name, "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)

            field_formats: dict = {}
            for key, row in enumerate(reader):

                if key == 0:
                    field_formats = row
                    continue

                query_text1 = f"INSERT INTO {table_name} ("

                query_text2 = ""
                for k, name in enumerate(row.keys()):
                    if k != 0:
                        query_text2 += " ,"
                    query_text2 += name

                query_text3 = f") VALUES (?{", ?" * (len(row.keys()) - 1)});"
                query_text = query_text1 + query_text2 + query_text3

                query_params = tuple(
                    [format_value(name, row[name], field_formats) for name in row.keys()]
                )

                cur.execute(query_text, query_params)
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"restoring document {str(err)}") from err
    finally:
        con.close()


def format_value(name: str, value: str, field_formats: dict):

    field_format: str = field_formats[name]
    if field_format == "bool":
        return 1 if value == "true" else 0
    elif field_format == "int":
        return int(value)
    else:
        return value
