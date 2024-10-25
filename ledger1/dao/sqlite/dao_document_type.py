import csv
import sqlite3
from ledger1.utils.fileio import read_text
from ledger1.dao.sqlite.dao import get_connection
from ledger1.document.document_type import DocumentType

def get():
    try:
        query_text: str = """
            SELECT
                id,
                name,
                at,
                active
            FROM document_type;
            """

        con, cur = get_connection()
        res = cur.execute(query_text)
        types = []
        for row in res.fetchall():
            types.append(DocumentType(
                id=str(row[0]),
                name=str(row[0]),
                at=str(row[2]),
                active=int(row[3]) == 1
            ))

        return types

    except sqlite3.DatabaseError as err:
        raise ValueError(f"getting document_type {str(err)}") from err
    finally:
        con.close()

def reset() -> None:
    """ Reset account1 table """

    try:

        query_text: str = read_text("./ledger1/dao/sqlite/document_type_reset.sql")

        con, cur = get_connection()
        cur.executescript(query_text)
        con.commit()

        with open("./ledger1/dao/csv/document_type.csv", "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for account in reader:
                cur.execute(
                    """
                    INSERT INTO document_type (
                        id,
                        name,
                        at,
                        active
                    ) VALUES (?, ?, ?, ?);
                    """,
                    (
                        str(account["id"]),
                        str(account["name"]),
                        str(account["at"]),
                        int(account["active"]) == 1,
                    )
                )
                con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"reseting document_type {str(err)}") from err
    finally:
        con.close()
