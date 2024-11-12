import sqlite3
import csv
from ledger1.utils import dbutil

def get_many(doc_type: str):

    con, cur = dbutil.get_connection()

    try:
        query_text = """
        SELECT
            d.doc_type,
            d.doc_num,
            a.name
        FROM document d
            INNER JOIN account1 a ON a.num = d.acc_num
        WHERE d.doc_type = ?
        """
        query_params = (doc_type,)

        cur.execute(query_text, query_params)
        rows = [dict(row) for row in cur.fetchall()]

        return rows

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting bank statements {str(err)}") from err
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
                    INSERT INTO document (
                        doc_type,
                        doc_num,
                        acc_num
                    ) VALUES (?, ?, ?);
                    """,
                    (
                        str(row["doc_type"]),
                        str(row["doc_num"]),
                        str(row["acc_num"])
                    )
                )
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"restoring document {str(err)}") from err
    finally:
        con.close()
