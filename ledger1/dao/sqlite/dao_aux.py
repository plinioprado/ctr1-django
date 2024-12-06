"""
crud generic sqlite tables returning Python lists or dictionaries

"""

import csv
import sqlite3
from ledger1.utils import dbutil


def get_many(table_name: str):

    con, cur = dbutil.get_connection()

    try:
        query_text = f"SELECT * FROM {table_name};"

        cur.execute(query_text)
        rows = [dict(row) for row in cur.fetchall()]

        return rows

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting {table_name}: {str(err)}") from err
    finally:
        con.close()


def get_one(table_name: str, record_id: int):

    con, cur = dbutil.get_connection()

    try:
        query_text = f"SELECT * FROM {table_name} WHERE id = ?"
        query_params = (record_id,)
        cur.execute(query_text, query_params)
        row = dict(cur.fetchone())

        return row

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting {table_name}: {str(err)}") from err
    finally:
        con.close()


def get_by_field(table_name: str, field_name: str, field_value: str | int):
    con, cur = dbutil.get_connection()

    try:
        query_text = f"SELECT * FROM {table_name} WHERE {field_name} = ?"
        query_params = (field_value,)
        cur.execute(query_text, query_params)
        row = dict(cur.fetchone())

        return row

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting {table_name}: {str(err)}") from err
    finally:
        con.close()


def restore(table_name: str, file_name: str, db_format: dict)-> None:
    """ Restore from CSV """

    con, cur = dbutil.get_connection()

    try:

        with open(file_name, "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for key, row in enumerate(reader):

                query_text1 = f"INSERT INTO {table_name} ("

                query_text2 = ""
                for k, name in enumerate(row.keys()):
                    if k != 0:
                        query_text2 += " ,"
                    query_text2 += name

                query_text3 = f") VALUES (?{", ?" * (len(row.keys()) - 1)});"
                query_text = query_text1 + query_text2 + query_text3

                query_params = tuple(
                    [format_value(name, row[name], db_format) for name in row.keys()]
                )

                cur.execute(query_text, query_params)
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"restoring document {str(err)}") from err
    finally:
        con.close()


def format_value(name: str, value: str, db_format: dict):

    field_format: str = db_format[name]
    if field_format == "bool":
        return 1 if value == "true" else 0
    elif field_format == "int":
        return int(value)
    else:
        return value
