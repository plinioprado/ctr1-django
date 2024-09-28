""" Data access object

Queries to get the operations from the ledger account business logic
and execure them in the SQLite database
"""

import csv
import sqlite3
from ledger1.models.account1 import Account1


def get_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Connect to the db and

    Returns:
        Tuple with sqlite3 connection and cursor objects
    """

    con = sqlite3.connect("ledger1/dao/sqlite/tws.sqlite3")
    cur = con.cursor()
    return con, cur


def get(acc_from: str, acc_to: str) -> list[dict]:
    """ Get (read) accounts """

    accs = []
    con, cur = get_connection()

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


def post(acc: Account1) -> str:
    """ Post (create) account """

    con, cur = get_connection()

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


def put(acc: Account1) -> str:
    """ Put (update) account """

    print(acc)

    con, cur = get_connection()

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


def delete(num: str) -> str:
    """ Delete account """

    con, cur = get_connection()

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


def reset() -> None:
    """ Reset account1 table """

    try:
        con, cur = get_connection()
        cur.execute("DROP TABLE IF EXISTS account1;")
        cur.execute(
            """CREATE TABLE IF NOT EXISTS account1 (
            num text PRIMARY KEY,
            name text,
            dc bool
            );""")
        con.commit()

        with open("ledger1/dao/csv/account.csv", "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for account in reader:
                cur.execute(
                    "INSERT INTO account1 (num, name, dc) VALUES (?, ?, ?);",
                    (account["num"], account["name"], account["dc"])
                )
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"Error reseting account {str(err)}") from err
    finally:
        con.close()
