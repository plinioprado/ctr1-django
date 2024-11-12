import csv
import sqlite3
from ledger1.document.invoice2 import Invoice2
from ledger1.utils import dbutil
from ledger1.utils import dateutil

def get_many() -> list[dict]:
    con, cur = dbutil.get_connection()

    try:

        query_text = """
            SELECT
                d.num,
                t.dt,
                d.cpart_name,
                d.descr,
                td.val as val_sale
                FROM invoice2 d
                    INNER JOIN transaction1_detail td ON
                        td.seq = 1 AND td.doc_type = "inv2" AND td.doc_num = d.num
                    INNER JOIN transaction1 t ON t.num = td.num
                ORDER BY d.num
            """

        cur.execute(query_text)
        invoices = []
        for row in cur.fetchall():
            invoices.append({
                "num": str(row["num"]),
                "dt": dateutil.date_timestamp_to_iso(row["dt"]),
                "cpart_name": str(row["cpart_name"]),
                "descr": str(row["descr"]),
                "val_sale": float(row["val_sale"]),
            })

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
                d.cpart_name,
                d.descr,
                t.num AS tra_num
                FROM invoice2 d
                    INNER JOIN transaction1_detail td ON
                        td.seq = 1 AND td.doc_type = "inv2" AND td.doc_num = d.num
                    INNER JOIN transaction1 t ON t.num = td.num
                WHERE d.num = ?
            """
        query_data = (num,)

        cur.execute(query_text, query_data)
        data = dict(cur.fetchone())

        if data is None:
            return None

        query_text = """
            SELECT
                td.account_num AS acc,
                td.val,
                td.dc,
                td.doc_type,
                td.doc_num
            FROM
                transaction1_detail td
            WHERE td.num = ?
            ORDER BY td.seq
            """
        query_data = (data["tra_num"],)
        cur.execute(query_text, query_data)

        seqs = []
        for row in cur.fetchall():
            seqs.append({
            "account": row["acc"],
            "val": float(row["val"]),
            "dc": row["dc"] == 1,
            "doc": { "type": row["doc_type"], "num": row["doc_num"] }
        })
        data["seqs"] = seqs
        invoice = Invoice2(data)

        return invoice
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
            cpart_name,
            descr,
            num
        )
        VALUES (?, ?, ?, ?);
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
            cpart_name = ?,
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

    con, cur = dbutil.get_connection()

    try:
        csv_filename = settings["invoice2"]["file_csv"]
        query_text: str = """
        INSERT INTO invoice2 (
            num,
            type,
            cpart_name,
            descr
        ) VALUES (?, ?, ?, ?);
        """

        con, cur = dbutil.get_connection()
        with open(csv_filename, "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for invoice in reader:
                query_data: tuple = (
                    invoice["num"],
                    invoice["type"],
                    invoice["cpart_name"],
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
