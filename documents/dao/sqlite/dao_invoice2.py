import csv
import sqlite3
from documents.invoice2.invoice2 import Invoice2
from documents.util import dateutil
from documents.util import dbutil

def get_many() -> list[Invoice2]:
    con, cur = dbutil.get_connection()

    try:
        query_text = """
            SELECT
                num,
                dt,
                type,
                seller_name,
                buyer_name,
                descr,
                val_sale,
                val_gst
                FROM invoice2
                ORDER BY num
            """
        invoices = []
        for row in cur.execute(query_text):
            invoices.append(Invoice2(row))

        return invoices

    except sqlite3.DatabaseError as err:
        raise ValueError(f"reseting account {str(err)}") from err
    except Exception as err:
        raise err
    finally:
        con.close()


def get_one(num: str) -> Invoice2:

    con, cur = dbutil.get_connection()

    try:
        query_text = """
            SELECT
                num,
                dt,
                type,
                seller_name,
                buyer_name,
                descr,
                val_sale,
                val_gst
                FROM invoice2
                WHERE num = ?
                ORDER BY num
            """
        query_data = (num,)

        cur.execute(query_text, query_data)
        row = cur.fetchone()

        if row is None:
            return None

        return Invoice2(row)
    except sqlite3.DatabaseError as err:
        raise ValueError(f"reseting account {str(err)}") from err
    except Exception as err:
        raise err
    finally:
        con.close()


def post(invoice: Invoice2) -> str:

    con, cur = dbutil.get_connection()

    try:
        query_text: str = """
        INSERT INTO invoice2 (
            dt,
            type,
            seller_name,
            buyer_name,
            descr,
            val_sale,
            val_gst,
            num
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        query_data = invoice.assqlitetuple()
        cur.execute(query_text, query_data)
        con.commit()

        last_num = invoice.num

        return last_num

    except sqlite3.DatabaseError as err:
        raise IOError(f"creating account {last_num}: {str(err)}") from err
    finally:
        con.close()


def put(invoice: Invoice2) -> None:

    con, cur = dbutil.get_connection()

    try:
        query_text = """
        UPDATE invoice2 SET
            dt = ?,
            type = ?,
            seller_name = ?,
            buyer_name = ?,
            descr = ?,
            val_sale = ?,
            val_gst = ?
        WHERE num = ?;
        """
        query_data = invoice.assqlitetuple()
        cur.execute(query_text, query_data)
        con.commit()

        return invoice.num

    except sqlite3.DatabaseError as err:
        raise IOError(f"updating invoice {invoice.num}: {str(err)}") from err
    finally:
        con.close()



def delete(num: str) -> str:
    """ Delete account """

    con, cur = dbutil.get_connection()

    try:
        query_text = "DELETE FROM invoice2 WHERE num = ?;"
        query_params = (num,)
        cur.execute(query_text, query_params)
        con.commit()

        return num

    except sqlite3.DatabaseError as err:
        raise IOError(f"deleting account {num}: {str(err)}") from err
    finally:
        con.close()


def restore(settings) -> None:
    """ Reset invoice2 table """

    try:
        csv_filename = settings["invoice2"]["file_csv"]
        query_text: str = """
        INSERT INTO invoice2 (
            num,
            dt,
            type,
            seller_name,
            buyer_name,
            descr,
            val_sale,
            val_gst
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """

        con, cur = dbutil.get_connection()
        with open(csv_filename, "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for invoice in reader:
                query_data: tuple = (
                    invoice["num"],
                    dateutil.date_iso_to_timestamp(invoice["dt"]),
                    invoice["type"],
                    invoice["seller_name"],
                    invoice["buyer_name"],
                    invoice["descr"],
                    invoice["val_sale"],
                    invoice["val_gst"]
                )
                cur.execute(query_text, query_data)
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"reseting account {str(err)}") from err
    except Exception as err:
        raise err
    finally:
        con.close()
