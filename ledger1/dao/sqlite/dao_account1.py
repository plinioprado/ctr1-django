""" Data access object

Queries to get the operations from the ledger account business logic
and execure them in the SQLite database
"""

import csv
import sqlite3
from ledger1.account.account1 import Account1
from ledger1.utils import dbutil


def get(db_id: str, acc_from: str, acc_to: str) -> list[dict]:
    """ Get (read) accounts """

    accs = []
    con, cur = dbutil.get_connection(db_id)

    try:
        query_text: str = """
        SELECT num, name, dc FROM account1
        WHERE num BETWEEN ? and ?;
        """
        query_params = (acc_from, acc_to)
        for row in cur.execute(query_text, query_params):

            acc = Account1(
                num=str(row[0]),
                name=str(row[1]),
                dc=row[2] == 1
            )
            accs.append({
                "num": acc.num,
                "name": acc.name,
                "dc": acc.dc
            })

        return accs

    except sqlite3.DatabaseError as err:
        raise IOError(f"getting accounts: {str(err)}") from err
    finally:
        con.close()


def post(db_id: str, acc: Account1) -> str:
    """ Post (create) account """

    con, cur = dbutil.get_connection(db_id)

    try:
        query_text: str = """
        INSERT INTO account1
        (num, name, dc)
        VALUES (?, ?, ?);
        """
        query_params = (acc.num, acc.name, 1 if acc.dc else 0)
        cur.execute(query_text, query_params)
        con.commit()

        return str(acc.num)

    except sqlite3.DatabaseError as err:
        raise IOError(f"creating account {acc.num}: {str(err)}") from err
    finally:
        con.close()


def put(db_id: str, acc: Account1) -> str:
    """ Put (update) account """

    con, cur = dbutil.get_connection(db_id)

    try:
        query_text = """
        UPDATE account1 SET
            name = ?,
            dc = ?
        WHERE num = ?;
        """
        query_params = (acc.name, 1 if acc.dc else 0, acc.num)
        cur.execute(query_text, query_params)
        con.commit()

        return str(acc.num)

    except sqlite3.DatabaseError as err:
        raise IOError(f"updating account1 {acc.num}: {str(err)}") from err
    finally:
        con.close()


def delete(db_id: str, num: str) -> str:
    """ Delete account """

    con, cur = dbutil.get_connection(db_id)

    try:
        query_text = "DELETE FROM account1 WHERE num = ?;"
        query_params = (num,)
        cur.execute(query_text, query_params)
        con.commit()

        return num

    except sqlite3.DatabaseError as err:
        raise IOError(f"deleting account {num}: {str(err)}") from err
    finally:
        con.close()


def get_options() -> list[dict]:
    """ Get a list of option for a form select

     """

    accs = []
    con, cur = dbutil.get_connection()

    try:
        query_text: str = """
        SELECT num, name FROM account1
        """
        for row in cur.execute(query_text):
            accs.append({
                "value": str(row[0]),
                "text": (row[1])
            })

        return accs

    except sqlite3.DatabaseError as err:
        raise IOError(f"getting accounts: {str(err)}") from err
    finally:
        con.close()


def restore() -> None:

    try:
        con, cur = dbutil.get_connection()

        with open("./ledger1/dao/csv/account.csv", "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for account in reader:
                cur.execute(
                    """
                    INSERT INTO account1 (
                        num,
                        name,
                        dc,
                        active,
                        doc_type,
                        doc_num
                    ) VALUES (?, ?, ?, ?, ?, ?);
                    """,
                    (
                        str(account["num"]),
                        str(account["name"]),
                        int(account["dc"]) == 1,
                        int(account["active"]) == 1,
                        str(account["doc_type"]),
                        str(account["doc_num"]),
                    )
                )
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"restoring account {str(err)}") from err
    except Exception as err:
        raise err
    finally:
        con.close()
