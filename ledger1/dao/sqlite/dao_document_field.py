import sqlite3
import csv
from ledger1.utils import dbutil


def get_one(
        db_id: str,
        doc_type: str,
        doc_num: str
    ) -> dict:

    con, cur = dbutil.get_connection(db_id)

    try:
        query_text = """
        SELECT
            doc_type,
            doc_num,
            field_group,
            field_name,
            field_value
        FROM document_field
        WHERE doc_type = ? AND doc_num = ?
        """
        query_params = (doc_type, doc_num)
        cur.execute(query_text, query_params)

        rows = {}
        for row in cur.fetchall():
            if row["field_group"] not in rows:
               rows[row["field_group"]] = {}
            rows[row["field_group"]][row["field_name"]] = row["field_value"]

        return rows

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting document field {str(err)}") from err
    finally:
        con.close()


def restore( db_id: str, filename: str) -> None:

    con, cur = dbutil.get_connection(db_id)

    try:
        with open(filename, "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cur.execute(
                    """
                    INSERT INTO document_field (
                        doc_type,
                        doc_num,
                        field_group,
                        field_name,
                        field_value
                    ) VALUES (?, ?, ?, ?, ?);
                    """,
                    (
                        str(row["doc_type"]),
                        str(row["doc_num"]),
                        str(row["field_group"]),
                        str(row["field_name"]),
                        str(row["field_value"]),
                    )
                )
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"restoring document field {str(err)}") from err
    finally:
        con.close()

