""" data access object from transaction to sqlite """

import csv
import sqlite3
from ledger1.dao.sqlite.util import get_connection
from ledger1.utils.field import date_iso_to_timestamp, date_timestamp_to_iso
from ledger1.models.transaction1 import Transaction1, Transaction1Seq

def get(num: int) -> Transaction1 | None:
    """ return one transaction """

    con, cur = get_connection()

    try:

        query_text: str = """
        SELECT
            td.num,
            t.dt AS date,
            t.descr,
            t.doc_type,
            t.doc_num,
            td.seq,
            td.account_num,
            td.val,
            td.dc
        FROM transaction1_detail td
        INNER JOIN transaction1 t ON t.num = td.num
        WHERE td.num = ?
        """
        query_data: tuple = (num,)

        seqs = []
        for row in cur.execute(query_text, query_data):
            if row[5] == 1:
                num = int(row[0])
                date: str = str(date_timestamp_to_iso(row[1]))
                descr: str = str(row[2])
                doc_type: str = str(row[3])
                doc_num: int = int(row[4])
            seqs.append(Transaction1Seq(
                seq=row[5],
                account=row[6],
                val=row[7],
                dc=row[8] == 1
            ))

        if len(seqs) == 0:
            return None

        tra = Transaction1(
            num,
            date,
            descr=descr,
            doc_type=doc_type,
            doc_num=doc_num,
            seqs=seqs
        )

        return tra

    except sqlite3.Error as err:
        raise IOError(f"Error getting transaction: {str(err)}") from err
    finally:
        con.close()


def post(tra: Transaction1) -> int | None:
    """ insert one transaction

    Args:
        tra (Transaction1): Object containing the transaction data without num

    Returns:
        int: num of the inserted transaction
    """

    con, cur = get_connection()

    try:
        query_text: str = """
        INSERT INTO transaction1
        (dt, descr, doc_type, doc_num)
        VALUES (?, ?, ?, ?);
        """
        query_params = (
            date_iso_to_timestamp(tra.date),
            tra.descr,
            tra.doc_type,
            tra.doc_num)
        cur.execute(query_text, query_params)

        last_num = cur.lastrowid

        query_text = """
        INSERT INTO transaction1_detail
        (num, seq, account_num, val, dc)
        VALUES (?, ?, ?, ?, ?);
        """
        query_data = [(last_num, seq.seq,  seq.account, seq.val, seq.dc) for seq in tra.seqs]
        cur.executemany(query_text, query_data)

        con.commit()

        return last_num

    except sqlite3.Error as err:
        raise IOError(f"Error creating transaction: {str(err)}") from err
    finally:
        con.close()


def put(tra: Transaction1):
    """ update one transaction

    Args:
        tra (Transaction1): Object containing the new data of the transaction

    Returns:
        int: num of the updated transaction
    """

    con, cur = get_connection()

    try:

        query_text = """
        UPDATE transaction1 SET
            dt = ?,
            descr = ?,
            doc_type = ?,
            doc_num = ?
        WHERE num = ?;
        """
        query_params = (
            date_iso_to_timestamp(tra.date),
            tra.descr,
            tra.doc_type,
            tra.doc_num,
            tra.num)
        cur.execute(query_text, query_params)

        cur.execute(f"DELETE FROM transaction1_detail WHERE num = {tra.num};")

        query_text = """
        INSERT INTO transaction1_detail
        (num, seq, account_num, val, dc)
        VALUES (?, ?, ?, ?, ?);
        """
        query_data = [(tra.num, seq.seq,  seq.account, seq.val, seq.dc) for seq in tra.seqs]
        cur.executemany(query_text, query_data)

        con.commit()

        return tra.num

    except sqlite3.Error as err:
        raise IOError(f"Error updating transaction {tra.num}: {str(err)}") from err
    finally:
        con.close()


def delete(num: int) -> int:
    """ Insert one transaction

    Args:
        num (int): number of the transaction to be deleted

    Returns:
        int: num of the deleted transaction
    """

    con, cur = get_connection()

    try:
        cur.execute(f"DELETE FROM transaction1 WHERE num = {num};")
        cur.execute(f"DELETE FROM transaction1_detail WHERE num = {num};")
        con.commit()

        return num

    except sqlite3.Error as err:
        raise IOError(f"Error deleting transaction {num}: {str(err)}") from err
    finally:
        con.close()


def reset() -> None:
    """ reset transaction table """

    con, cur = get_connection()

    try:
        cur.execute('''DROP TABLE IF EXISTS transaction1;''')
        cur.execute('''CREATE TABLE IF NOT EXISTS transaction1 (
            num INTEGER PRIMARY KEY,
            dt REAL,
            descr TEXT,
            doc_type TEXT,
            doc_num, INTEGER
        );''')
        con.commit()

        with open(
            "ledger1/dao/csv/transaction1.csv",
            "r",
            encoding="UTF-8"
        ) as csvfile:

            reader = csv.DictReader(csvfile)
            for row in reader:

                cur.execute(
                    """
                    INSERT INTO transaction1 (num, dt, descr, doc_type, doc_num)
                        VALUES (?, ?, ?, ?, ?);
                    """,
                    (
                        int(row["num"]),
                        date_iso_to_timestamp(row["dt"]),
                        str(row["descr"]),
                        str(row["doc_type"]),
                        int(row["doc_num"])
                    )
                )
                con.commit()

        cur.execute('''DROP TABLE IF EXISTS transaction1_detail;''')
        cur.execute('''CREATE TABLE IF NOT EXISTS transaction1_detail (
            num INTEGER,
            seq INTEGER,
            account_num text,
            val real,
            dc BOOL
        );''')

        with open("ledger1/dao/csv/transaction1_detail.csv", "r", encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cur.execute(
                    """
                    INSERT INTO transaction1_detail (
                        num,
                        seq,
                        account_num,
                        val,
                        dc
                    ) VALUES (?, ?, ?, ?, ?);
                    """,
                    (
                        int(row["num"]),
                        int(row["seq"]),
                        str(row["account_num"]),
                        float(row["val"]),
                        row["dc"] == "True"
                    )
                )
                con.commit()

    except sqlite3.Error as err:
        raise IOError(f"Error resetting transaction: {str(err)}") from err
    finally:
        con.close()
