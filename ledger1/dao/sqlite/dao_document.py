import sqlite3
import csv
from ledger1.dao.sqlite import dao
from ledger1.dao.sqlite.dao import get_connection
from ledger1.document.document1 import Document1
from ledger1.utils.field import date_timestamp_to_iso

def get(doc_type):

    try:
        con, cur = dao.get_connection()

        query_text = """
        SELECT
            td.doc_num,
            t.dt,
            td.val,
            d.cpart_name
        FROM transaction1_detail td
            INNER JOIN transaction1 t ON t.num = td.num
            INNER JOIN document d ON d.type_id = td.doc_type AND d.num = td.doc_num
        WHERE td.doc_type = ?
        """
        query_params = (doc_type,)
        cur.execute(query_text, query_params)

        docs = []
        for row in cur.fetchall():

            docs.append(
                Document1(
                    num=str(row[0]),
                    date=date_timestamp_to_iso(row[1]),
                    val=float(row[2]),
                    cpart_name=(row[3])
                )
            )

        return docs

    except sqlite3.DatabaseError as err:
        raise IOError(f"getting accounts: {str(err)}") from err
    finally:
        con.close()


def reset() -> None:
    """ reset transaction table """

    con, cur = get_connection()

    try:
        with open(
            "ledger1/dao/csv/document.csv",
            "r",
            encoding="UTF-8"
        ) as csvfile:

            reader = csv.DictReader(csvfile)
            for row in reader:

                cur.execute(
                    """
                    INSERT INTO document (type_id, num, cpart_name)
                        VALUES (?, ?, ?);
                    """,
                    (
                        str(row["type_id"]),
                        str(row["num"]),
                        str(row["cpart_name"])
                    )
                )
                con.commit()

    except sqlite3.Error as err:
        raise IOError(f"Error resetting document: {str(err)}") from err
    finally:
        con.close()
