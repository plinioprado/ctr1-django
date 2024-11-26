"""
document table will complement transaction table to feed the document various objects
linked by tra_seq.doc_type + tra_seqdoc.num
"""


import sqlite3
import csv
from ledger1.utils import dbutil
from ledger1.utils import dateutil


def get_many(doc_type: str = None) -> list[dict]:

    con, cur = dbutil.get_connection()

    try:

        query_text = """
        SELECT
            d.doc_type,
            d.doc_num,
            a.name
        FROM document d
            INNER JOIN account1 a ON a.num = d.acc_num
        WHERE d.doc_type LIKE ?
        """
        doc_type_param = "%" if doc_type is None else doc_type
        query_params = (doc_type_param,)

        cur.execute(query_text, query_params)
        rows = [dict(row) for row in cur.fetchall()]

        return rows

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting bank statements {str(err)}") from err
    finally:
        con.close()


def get_many_tra(doc_dc: bool, doc_type: str):

    con, cur = dbutil.get_connection()

    try:
        query_text: str = """
        SELECT
            td.doc_type,
            td.doc_num,
            td.dc,
            t.dt,
            d.cpart_name,
            t.descr,
            td.val
        FROM transaction1_detail td
            INNER JOIN transaction1 t ON t.num = td.num
            INNER JOIN document d
                ON d.doc_type = td.doc_type AND d.doc_num = td.doc_num
        WHERE td.doc_type = ? AND td.dc = ?
        """

        query_params: str = (doc_type, int(doc_dc))
        cur.execute(query_text, query_params)

        data = []
        for row in cur.execute(query_text, query_params):
            data.append({
                "doc_type": row["doc_type"],
                "doc_num": row["doc_num"],
                "doc_dc": row["dc"] == 1,
                "dt": dateutil.date_timestamp_to_iso(row["dt"]),
                "cpart_name": row["cpart_name"],
                "descr": row["descr"],
                "val": row["val"],
            })

        return data
    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting documents {str(err)}") from err
    finally:
        con.close()


def get_one(doc_type: str, doc_num: str) -> dict:

    con, cur = dbutil.get_connection()

    try:
        query_text = """
        SELECT
            d.doc_type,
            d.doc_num,
            d.acc_num,
            d.cpart_name,
            a.name
        FROM document d
            LEFT JOIN account1 a ON a.num = d.acc_num
        WHERE d.doc_type = ? AND d.doc_num = ?
        """
        query_params = (doc_type, doc_num)
        cur.execute(query_text, query_params)
        row = dict(cur.fetchone())

        return row

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting bank statements {str(err)}") from err
    finally:
        con.close()


def post(data: dict):

    con, cur = dbutil.get_connection()

    try:
        query_text: str = """
        INSERT INTO document (
            doc_type,
            doc_num,
            cpart_name
        )
        VALUES (?, ?, ?);
        """
        query_params = (data["doc_type"],data["doc_num"],data["cpart_name"])
        cur.execute(query_text, query_params)

        if data["fields"]:
            query_text2: str = """
            INSERT INTO document_field (
                doc_type,
                doc_num,
                field_group,
                field_name,
                field_value
            )
            VALUES (?, ?, ?, ?, ?);
            """

            for field_group in data["fields"]:
                for field_name in data["fields"][field_group]:
                    query_params2 = (
                        data["doc_type"],
                        data["doc_num"],
                        field_group,
                        field_name,
                        data["fields"][field_group][field_name]
                    )
                    cur.execute(query_text2, query_params2)

        con.commit()

        return {"doc_type": data["doc_type"],"doc_num": data["doc_num"]}

    except sqlite3.DatabaseError as err:
        raise IOError(f"creating document {data["doc_type"]} {data["doc_num"]}: {str(err)}") from err
    finally:
        con.close()


def put(data: dict):

    con, cur = dbutil.get_connection()

    try:
        query_text: str = """
        UPDATE document
        SET
            cpart_name = ?
        WHERE doc_type = ? AND doc_num = ?;
        """
        query_params = (data["cpart_name"],data["doc_type"],data["doc_num"])
        cur.execute(query_text, query_params)

        query_text2: str = """
        UPDATE document_field
        SET
            field_value = ?
        WHERE
            doc_type = ? AND
            doc_num = ? AND
            field_group = ? AND
            field_name = ?
        """
        for field_group in data["fields"]:
            for field_name in data["fields"][field_group]:
                query_params2 = (
                    data["fields"][field_group][field_name],
                    data["doc_type"],
                    data["doc_num"],
                    field_group,
                    field_name,
                )
                cur.execute(query_text2, query_params2)

        con.commit()

        return {"doc_type": data["doc_type"],"doc_num": data["doc_num"]}

    except sqlite3.DatabaseError as err:
        raise IOError(f"updating document {data["doc_type"]} {data["doc_num"]}: {str(err)}") from err
    finally:
        con.close()


def delete(doc_type: str, doc_num: str):

    con, cur = dbutil.get_connection()

    try:
        query_text = """
        DELETE FROM document
        WHERE doc_type = ? AND doc_num = ?;
        """
        query_params = (doc_type, doc_num)
        cur.execute(query_text, query_params)

        query_text2 = """
        DELETE FROM document_field
        WHERE doc_type = ? AND doc_num = ?;
        """
        cur.execute(query_text2, query_params)

        con.commit()

        return (doc_type,doc_num)

    except sqlite3.DatabaseError as err:
        raise IOError(f"deleting document {doc_type} {doc_num}: {str(err)}") from err
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
                        acc_num,
                        cpart_name
                    ) VALUES (?, ?, ?, ?);
                    """,
                    (
                        str(row["doc_type"]),
                        str(row["doc_num"]),
                        str(row["acc_num"]),
                        str(row["cpart_name"])
                    )
                )
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"restoring document {str(err)}") from err
    finally:
        con.close()
