import csv
import sqlite3
from ledger1.utils import dbutil
from ledger1.document.document_type import DocumentType

def get(db_id: str) -> list[DocumentType]:
    try:
        con, cur = dbutil.get_connection(db_id)

        query_text: str = """
            SELECT
                id,
                name,
                num_on_seq,
                dc_false_name,
                dc_true_name,
                cpart_role_d,
                cpart_role_c,
                active
            FROM document_type;
            """

        res = cur.execute(query_text)
        types = []
        for row in res.fetchall():
            types.append(DocumentType(
                id=str(row["id"]),
                name=str(row["name"]),
                num_on_seq=str(row["num_on_seq"]),
                dc_false_name=str(row["dc_false_name"]),
                dc_true_name=str(row["dc_true_name"]),
                cpart_role_d=str(row["cpart_role_d"]),
                cpart_role_c=str(row["cpart_role_c"]),
                active=int(row["active"]) == 1
            ))
        return types

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting document_type {str(err)}") from err
    finally:
        con.close()


def reset(db_id: str) -> None:
    """ Reset account1 table """

    try:
        con, cur = dbutil.get_connection(db_id)

        with open("./ledger1/dao/csv/document_type.csv", "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for doc_type in reader:
                cur.execute(
                    """
                    INSERT INTO document_type (
                        id,
                        name,
                        traacc,
                        num_on_seq,
                        dc_true_name,
                        dc_false_name,
                        cpart_role_d,
                        cpart_role_c,
                        active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        str(doc_type["id"]),
                        str(doc_type["name"]),
                        int(doc_type["traacc"]) == 1,
                        str(doc_type["num_on_seq"]),
                        str(doc_type["dc_true_name"]),
                        str(doc_type["dc_false_name"]),
                        str(doc_type["cpart_role_d"]),
                        str(doc_type["cpart_role_c"]),
                        int(doc_type["active"]) == 1,
                    )
                )
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"reseting document_type {str(err)}") from err
    finally:
        con.close()
