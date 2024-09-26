""" Data access object for a SQLite db in invoice1.db using SQL queries"""

import sqlite3
from invoice1.invoice1_model import Invoice1Model


def get_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Connect to the db and

    Returns:
        Tuple with sqlite3 connection and cursor objects
    """

    con = sqlite3.connect("invoice1/db.sqlite3")
    cur = con.cursor()
    return con, cur


def reset() -> None:
    """
    Recreate the invoice1 db with default data
    """

    con, cur = get_connection()
    cur.execute('''DROP TABLE IF EXISTS invoice1;''')
    cur.execute('''CREATE TABLE IF NOT EXISTS invoice1 (
        num integer PRIMARY KEY,
        value real,
        issue_date text,
        parts_seller_name text,
        parts_buyer_name text,
        status text
    );''')
    cur.execute('''INSERT INTO invoice1
        (num, value, issue_date, parts_seller_name, parts_buyer_name, status)
        VALUES
        (
            NULL,
            1000,
            "2020-01-15",
            "Example Ltd",
            "Cedar stores Ltd.",
            "open"
        ),
        (
            NULL,
            1200,
            "2020-01-16",
            "Example Ltd",
            "Mahogany Manufacturing Ltd.",
            "open"
        )
        ;''')
    con.commit()


def get() -> list[Invoice1Model]:
    """
    Read (get) all invoices

    Returns:
        List of Invoice1 objects with all records
    """

    con, cur = get_connection()
    try:
        invoices = []
        for row in cur.execute('''SELECT
                num, value, issue_date, parts_seller_name, parts_buyer_name, status
                FROM invoice1
            '''):
            invoice = Invoice1Model({
                "num": int(row[0]),
                "value": float(row[1]),
                "issue_date": str(row[2]),
                "parts_seller_name": str(row[3]),
                "parts_buyer_name": str(row[4]),
                "status": str(row[5]),
            })
            invoices.append(invoice)
        return invoices
    except Exception as err:
        raise IOError("reading invoice") from err
    finally:
        con.close()


def get_by_num(num: int) -> Invoice1Model:
    """
    Read (get) the requesed invoice

    Args:
        num: number of the requested invoice

    Returns:
        Invoice1 object with the requested record
    """

    con, cur = get_connection()

    try:
        query_text = '''SELECT
                num, value, issue_date, parts_seller_name, parts_buyer_name, status
                FROM invoice1 WHERE num = ?
            '''
        cur.execute(query_text, (num,))
        row = cur.fetchone()

        if row is None:
            return None

        invoice = Invoice1Model({
                "num": int(row[0]),
                "value": float(row[1]),
                "issue_date": str(row[2]),
                "parts_seller_name": str(row[3]),
                "parts_buyer_name": str(row[4]),
                "status": str(row[5]),
        })
        return invoice
    except Exception as err:
        raise IOError("reading invoice") from err
    finally:
        con.close()


def post(invoice: Invoice1Model) -> dict[str, int]:
    """
    Create (post) a new invoice

    Args:
        invoice: data to be created

    Returns:
        dict with the number of the created invoice
    """

    con, cur = get_connection()
    try:
        query_data = (
            invoice.value,
            invoice.issue_date,
            invoice.parts_seller_name,
            invoice.parts_buyer_name,
            invoice.status
        )
        query_text = """INSERT INTO
            invoice1 (value, issue_date, parts_seller_name, parts_buyer_name, status)
            VALUES (?, ?, ?, ?, ?);"""
        cur.execute(query_text, query_data)
        con.commit()

        if cur.lastrowid is None:
            raise IOError

        return {"num": int(cur.lastrowid)}
    except Exception as err:
        raise IOError("creating invoice") from err
    finally:
        con.close()


def put(invoice: Invoice1Model) -> dict[str, int]:
    """
    Update (put) an invoice

    Args:
        invoice: data to replace in the invoice of that num

    Returns:
        dict with the number of the updated invoice
    """

    con, cur = get_connection()
    try:
        query_data = (
            invoice.value,
            invoice.issue_date,
            invoice.parts_seller_name,
            invoice.parts_buyer_name,
            invoice.status,
            invoice.num,
        )
        query_text = """UPDATE invoice1 SET
            value = ?,
            issue_date = ?,
            parts_seller_name = ?,
            parts_buyer_name = ?,
            status = ?
            WHERE num = ?"""
        cur.execute(query_text, query_data)
        con.commit()

        return {"num": invoice.num}
    except Exception as err:
        raise IOError("updating invoice") from err
    finally:
        con.close()


def delete(num: int):
    """
    Delete an invoice

    Args:
        num: num of the invoice to be deleted

    Returns:
        number of the deleted invoice
    """

    con, cur = get_connection()
    try:
        query_data = tuple(str(num))
        query_text = """DELETE FROM invoice1 WHERE num = ?"""
        cur.execute(query_text, query_data)
        con.commit()

        return num
    except Exception as err:
        raise IOError("deleting invoice") from err
    finally:
        con.close()
