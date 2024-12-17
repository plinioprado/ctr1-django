import sqlite3
import csv
from ledger1.utils import dbutil


def get_many(query: dict) -> list[dict]:

    key = query["key"] if "key" in query.keys() else ""

    con, cur = dbutil.get_connection()

    try:
        query_text = """
        SELECT
            setting_key,
            setting_value
        FROM setting
        WHERE setting_key LIKE ?
        """
        query_params = (f"{key}%",)

        cur.execute(query_text, query_params)
        rows: list[dict] = []
        for row in cur.fetchall():
            rows.append({
                "key": row["setting_key"],
                "value": row["setting_value"]
            })

        return rows

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting settings {str(err)}") from err
    finally:
        con.close()


def get_one(key: str):

    con, cur = dbutil.get_connection()

    try:
        query_text = """
        SELECT
            setting_key,
            setting_value
        FROM setting
        WHERE setting_key = ?
        """
        query_params = (key,)

        cur.execute(query_text, query_params)
        row: dict = dict(cur.fetchone())

        print(row)

        return row

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting setting {str(err)}") from err
    finally:
        con.close()


def restore(file_name) -> None:
    """ Restore from CSV """

    con, cur = dbutil.get_connection()

    try:
        with open(file_name, "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cur.execute(
                    """
                    INSERT INTO setting (
                        setting_key,
                        setting_value
                    ) VALUES (?, ?);
                    """,
                    (
                        str(row["setting_key"]),
                        str(row["setting_value"])
                    )
                )
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"restoring setting {str(err)}") from err
    finally:
        con.close()
