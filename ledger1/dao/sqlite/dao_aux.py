"""
crud generic sqlite tables returning Python lists or dictionaries

"""

import csv
import sqlite3
from ledger1.admin.aux import Aux
from ledger1.utils import dbutil


def get_many(obj: Aux, filters: dict, db_id: str) -> list[dict]:
    """ accepts one filter using LIKE """

    con, cur = dbutil.get_connection(db_id)

    try:
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


def get_one(obj: Aux, record_id: str, db_id: str):

    con, cur = dbutil.get_connection(db_id)

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


def get_by_field(table_name: str, field_name: str, field_value: str | int, db_id: str) -> dict:

    con, cur = dbutil.get_connection(db_id)

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


def post(obj: Aux, db_id: str) -> int:

    con, cur = dbutil.get_connection(db_id)

    try:
        data = obj.get_to_db()
        db_format = obj.get_db_format()

        query_text1 = f"INSERT INTO {obj.table_name} ("
        query_text2 = ""
        for k, name in enumerate(data.keys()):
            if k != 0:
                query_text2 += " ,"
            query_text2 += name
        query_text3 = f") VALUES (?{", ?" * (len(db_format) - 1)});"
        query_text = query_text1 + query_text2 + query_text3

        query_params = tuple(
            [format_value(name, data[name], db_format) for name in db_format.keys()])

        cur.execute(query_text, query_params)
        con.commit()

        last_id = data[obj.primary_key]
        if last_id is None:
            last_id = cur.lastrowid

        return last_id

    except sqlite3.DatabaseError as err:
        raise IOError(f"creating {obj.table_name}: {str(err)}") from err
    finally:
        con.close()


def put(obj: Aux, db_id: str) -> int:

    con, cur = dbutil.get_connection(db_id)

    try:
        data = obj.get_to_db()
        db_format = obj.get_db_format()
        names: list = [name for name in db_format if name != obj.primary_key]
        values: list = [format_value(name, data[name], db_format)  for name in db_format if name != obj.primary_key] + [data[obj.primary_key]]

        query_text1 = f"UPDATE {obj.table_name} SET "
        query_text2 = ""
        for k, name in enumerate(names):
            if name == "id":
                continue
            if k > 0:
                query_text2 += ", "
            query_text2 += f"{name} = ?"
        query_text3 = f" WHERE {obj.primary_key} = ?;"
        query_text = query_text1 + query_text2 + query_text3
        query_params = tuple(values)

        cur.execute(query_text, query_params)
        con.commit()

        return data[obj.primary_key]

    except sqlite3.DatabaseError as err:
        raise IOError(f"updating {obj.table_name} {data[obj.primary_key]}") from err
    finally:
        con.close()


def delete(record_id: str, obj: Aux, db_id: str) -> str:

    con, cur = dbutil.get_connection(db_id)

    try:
        query_text = f"DELETE FROM {obj.table_name} WHERE {obj.primary_key} = ?;"
        query_params = (record_id,)

        cur.execute(query_text, query_params)
        con.commit()

        return record_id

    except sqlite3.DatabaseError as err:
        raise IOError(f"deleting {obj.table_name} {record_id}") from err
    finally:
        con.close()


def restore(
        db_id: str,
        table_name: str,
        file_name: str,
        db_format: dict
    )-> None:
    """ Restore from CSV """

    con, cur = dbutil.get_connection(db_id)

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

    try:
        field_format: str = db_format[name]
        if value is None:
            return None
        elif field_format == "bool":
            return 1 if value == "true" else 0
        elif field_format == "int":
            return int(value)
        else:
            return value

    except ValueError as err:
        raise ValueError(f"converting field {name}") from err
