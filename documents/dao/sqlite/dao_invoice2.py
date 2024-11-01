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
            invoices.append(Invoice2(
                num=str(row["num"]),
                dt=dateutil.date_timestamp_to_iso(row["dt"]),
                type=str(row["type"]),
                seller_name=str(row["seller_name"]),
                buyer_name=str(row["buyer_name"]),
                descr=str(row["descr"]),
                val_sale=float(row["val_sale"]),
                val_gst=float(row["val_gst"])
            ))

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

        return Invoice2(
                num=str(row["num"]),
                dt=dateutil.date_timestamp_to_iso(row["dt"]),
                type=str(row["type"]),
                seller_name=str(row["seller_name"]),
                buyer_name=str(row["buyer_name"]),
                descr=str(row["descr"]),
                val_sale=float(row["val_sale"]),
                val_gst=float(row["val_gst"])
            )
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
