import csv
import sqlite3
from documents.invoice2.invoice2 import Invoice2
from documents.util import dbutil

def get_many() -> list[Invoice2]:
    con, cur = dbutil.get_connection()

    try:

        query_text = """
            SELECT
                d.num,
                t.dt,
                d.type,
                d.seller_name,
                d.buyer_name,
                d.descr,
                td.val as val_sale,
                (SELECT td2.val
                FROM transaction1_detail td2
                WHERE td2.num = t.num AND td2.seq = 2)
                AS val_gst
                FROM invoice2 d
                    INNER JOIN transaction1_detail td ON
                        td.seq = 1 AND td.doc_type = "inv2" AND td.doc_num = d.num
                    INNER JOIN transaction1 t ON t.num = td.num
                ORDER BY d.num
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
                d.num,
                t.dt,
                d.type,
                d.seller_name,
                d.buyer_name,
                d.descr,
                td.val as val_sale,
                (SELECT td2.val
                FROM transaction1_detail td2
                WHERE td2.num = t.num AND td2.seq = 2)
                AS val_gst
                FROM invoice2 d
                    INNER JOIN transaction1_detail td ON
                        td.seq = 1 AND td.doc_type = "inv2" AND td.doc_num = d.num
                    INNER JOIN transaction1 t ON t.num = td.num
                WHERE d.num = ?
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
            type,
            seller_name,
            buyer_name,
            descr,
            num
        )
        VALUES (?, ?, ?, ?, ?);
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
            type = ?,
            seller_name = ?,
            buyer_name = ?,
            descr = ?
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


def get_tra_num(doc_num: str) -> int:
    con, cur = dbutil.get_connection()

    try:
        query_text = """
            SELECT num
            FROM transaction1_detail
            WHERE
                seq = 1 AND
                doc_type = "inv2" AND
                doc_num = ?
            """
        query_data = (doc_num,)

        cur.execute(query_text, query_data)
        row = cur.fetchone()

        return int(row["num"])

    except sqlite3.DatabaseError as err:
        raise ValueError(f"reseting account {str(err)}") from err
    except Exception as err:
        raise err
    finally:
        con.close()


def restore(settings) -> None:
    """ Reset invoice2 table """

    try:
        csv_filename = settings["invoice2"]["file_csv"]
        query_text: str = """
        INSERT INTO invoice2 (
            num,
            type,
            seller_name,
            buyer_name,
            descr
        ) VALUES (?, ?, ?, ?, ?);
        """

        con, cur = dbutil.get_connection()
        with open(csv_filename, "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for invoice in reader:
                query_data: tuple = (
                    invoice["num"],
                    invoice["type"],
                    invoice["seller_name"],
                    invoice["buyer_name"],
                    invoice["descr"],
                )
                cur.execute(query_text, query_data)
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"reseting account {str(err)}") from err
    except Exception as err:
        raise err
    finally:
        con.close()
