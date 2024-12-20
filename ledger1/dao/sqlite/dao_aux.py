"""
crud generic sqlite tables returning Python lists or dictionaries

"""

import csv
import sqlite3
from ledger1.utils import dbutil


def get_many(obj: object, filters: dict):

    con, cur = dbutil.get_connection()

    try:


        # will work for one filter using LIKE
        filter_value: list = list(filters.values())[0] if filters else []

        query_filters = f" WHERE {obj.filter_field} LIKE ?" if filters else ""
        query_text: str = f"SELECT * FROM {obj.table_name}{query_filters};"
        query_params = (f"{filter_value}%",) if filters else ()

        cur.execute(query_text, query_params)
        rows = [dict(row) for row in cur.fetchall()]

        return rows

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting {obj.table_name}: {str(err)}") from err
    finally:
        con.close()


def get_one(obj: object, record_id: str):

    con, cur = dbutil.get_connection()

    try:
        query_text = f"SELECT * FROM {obj.table_name} WHERE {obj.primary_key} = ?"
        query_params = (record_id,)
        cur.execute(query_text, query_params)
        row = dict(cur.fetchone())

        return row

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting {obj.table_name}: {str(err)}") from err
    finally:
        con.close()


def get_by_field(table_name: str, field_name: str, field_value: str | int) -> dict:
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


def post(table_name: str, data: dict, db_format: dict) -> int:

    con, cur = dbutil.get_connection()

    try:
        query_text1 = f"INSERT INTO {table_name} ("
        query_text2 = ""
        for k, name in enumerate(data.keys()):
            if k != 0:
                query_text2 += " ,"
            query_text2 += name
        query_text3 = f") VALUES (?{", ?" * (len(data.keys()) - 1)});"
        query_text = query_text1 + query_text2 + query_text3

        query_params = tuple(
            [format_value(name, data[name], db_format) for name in data.keys()])

        cur.execute(query_text, query_params)
        con.commit()

        last_num = cur.lastrowid

        return last_num

    except sqlite3.DatabaseError as err:
        raise IOError(f"creating document {data["doc_type"]} {data["doc_num"]}: {str(err)}") from err
    finally:
        con.close()



def put(table_name: str, data: dict, db_format: dict) -> int:

    con, cur = dbutil.get_connection()

    try:
        query_text1 = f"UPDATE {table_name} SET "
        query_text2 = ""
        for k, name in enumerate(data.keys()):
            if name == "id":
                continue
            if k > 1:
                query_text2 += ", "
            query_text2 += f"{name} = ?"
        query_text3 = " WHERE id = ?;"
        query_text = query_text1 + query_text2 + query_text3

        values: list = list(data.values())[1:] + [data["id"]]
        query_params = tuple(values)

        cur.execute(query_text, query_params)
        con.commit()

        return data["id"]

    except sqlite3.DatabaseError as err:
        raise IOError(f"updating {table_name} {data["id"]}") from err
    finally:
        con.close()


def delete(table_name: str, record_id: str):

    con, cur = dbutil.get_connection()

    try:
        query_text = f"DELETE FROM {table_name} WHERE id = ?;"
        query_params = (record_id,)

        cur.execute(query_text, query_params)
        con.commit()

        return record_id

    except sqlite3.DatabaseError as err:
        raise IOError(f"deleting {table_name} {record_id}") from err
    finally:
        con.close()


def restore(table_name: str, file_name: str, db_format: dict)-> None:
    """ Restore from CSV """

    con, cur = dbutil.get_connection()

    try:

        with open(file_name, "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # if id is None, autonum
                names = [name for name in db_format.keys() if (name != "id" or name in row)]

                query_text1 = f"INSERT INTO {table_name} ("
                query_text2 = ""
                for name in names:
                    if query_text2 != "":
                        query_text2 += ", "
                    query_text2 += name
                query_text3 = f") VALUES (?{", ?" * (len(names) - 1)});"
                query_text = query_text1 + query_text2 + query_text3

                query_params = tuple(
                    [format_value(name, row[name], db_format) for name in names]
                )
                cur.execute(query_text, query_params)
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"restoring {table_name} {str(err)}") from err
    finally:
        con.close()


def format_value(name: str, value: str, db_format: dict):

    field_format: str = db_format[name]
    if value is None:
        return None
    elif field_format == "bool":
        return 1 if value == "true" else 0
    elif field_format == "int":
        return int(value)
    else:
        return value
