""" data access object from transaction to sqlite """

import csv
import sqlite3
from ledger1.transaction.transaction import Transaction, TransactionSeq, TransactionSeqDoc
from ledger1.utils import dbutil
from ledger1.utils import dateutil


# get

def get_many(db_id: str, date_from: str, date_to: str) -> Transaction | None:
    """ return one transaction """

    con, cur = dbutil.get_connection(db_id)

    try:

        query_text: str = """
        SELECT
            td.num,
            t.dt AS date,
            t.descr,
            td.seq,
            td.account_num,
            td.val,
            td.dc,
            td.doc_type,
            td.doc_num
        FROM transaction1_detail td
            INNER JOIN transaction1 t ON t.num = td.num
        WHERE t.dt BETWEEN ? AND ?
        ORDER BY td.num, td.seq DESC
        """

        query_data: tuple = (
            dateutil.date_iso_to_timestamp(date_from),
            dateutil.date_iso_to_timestamp(date_to),
        )

        seqs = []
        tras = []
        for row in cur.execute(query_text, query_data):

            num = int(row[0])
            date: str = dateutil.date_timestamp_to_iso(row[1])
            descr: str = str(row[2])
            seq: int = int(row[3])
            account: str = row[4]
            val=row[5]
            dc: bool = row[6] == 1

            seqs.insert(
                0, TransactionSeq(
                    account,
                    val,
                    dc,
                    doc=TransactionSeqDoc(
                        type=str(row[7]),
                        num=str(row[8])
                    )
                )
            )

            if seq == 1:
                tras.insert(0, Transaction(
                    num,
                    date,
                    descr,
                    seqs))
                seqs = []

        return tras[::-1]

    except sqlite3.Error as err:
        raise IOError(f"Error getting transaction: {str(err)}") from err
    finally:
        con.close()


def get_many_by_doc(db_id: str, doc_type: str, doc_dc) -> list[dict]:

    con, cur = dbutil.get_connection(db_id)

    try:
        query_text: str = """
        SELECT
            td.doc_type,
            td.doc_num,
            td.dc,
            t.dt,
            t.descr,
            td.val
        FROM transaction1_detail td
            INNER JOIN transaction1 t ON t.num = td.num
        WHERE td.doc_type = ? AND td.dc = ?
        ORDER BY td.num, td.seq DESC
        """

        query_params: tuple = (doc_type, doc_dc)

        data = []
        for row in cur.execute(query_text, query_params):
            data.append({
                "doc_type": row["doc_type"],
                "doc_num": row["doc_num"],
                "doc_dc": row["dc"] == 1,
                "dt": dateutil.date_timestamp_to_iso(row["dt"]),
                "descr": row["descr"],
                "val": row["val"],
            })

        return data

    except sqlite3.Error as err:
        raise IOError(f"Error getting transaction: {str(err)}") from err
    finally:
        con.close()


def get_many_by_acc(db_id: str, acc_num: str) -> list[dict]:
    """ return one transaction """

    con, cur = dbutil.get_connection(db_id)

    try:

        query_text: str = """
        SELECT
            td.num,
            t.dt AS date,
            t.descr,
            td.seq,
            td.account_num,
            td.val,
            td.dc,
            td.doc_type,
            td.doc_num
        FROM transaction1_detail td
            INNER JOIN transaction1 t ON t.num = td.num
        WHERE td.account_num = ?
        ORDER BY td.num, td.seq DESC
        """

        query_params: tuple = (acc_num,)
        cur.execute(query_text, query_params)
        rows = cur.fetchall()
        tras = [dict(row) for row in rows]

        return tras


    except sqlite3.Error as err:
        raise IOError(f"Error getting transaction: {str(err)}") from err
    finally:
        con.close()


def get_one(db_id: str, num: int) -> Transaction | None:
    """ return one transaction """

    con, cur = dbutil.get_connection(db_id)

    try:
        query_text: str = """
        SELECT
            td.num,
            t.dt AS date,
            t.descr,
            td.seq,
            td.account_num,
            td.val,
            td.dc,
            td.doc_type,
            td.doc_num
        FROM transaction1_detail td
            INNER JOIN transaction1 t ON t.num = td.num
        WHERE td.num = ?
        """
        query_data: tuple = (num,)

        date = None,
        descr = None
        seqs = []
        for row in cur.execute(query_text, query_data):
            if row[3] == 1:
                num = int(row[0])
                date: str = dateutil.date_timestamp_to_iso(row[1])
                descr: str = str(row[2])
            seqs.append(TransactionSeq(
                account=row[4],
                val=row[5],
                dc=row[6] == 1,
                doc=TransactionSeqDoc(
                    type=row[7],
                    num=row[8]
                )
            ))

        if len(seqs) == 0:
            return None

        else:
            return Transaction(
                num,
                date,
                descr=descr,
                seqs=seqs)


    except sqlite3.Error as err:
        raise IOError(f"getting transaction: {str(err)}") from err
    finally:
        con.close()


def get_num_by_doc(db_id: str, doc_type: str, doc_num: str) -> int:
    con, cur = dbutil.get_connection(db_id)

    try:
        query_text: str = """
        SELECT num
        FROM transaction1_detail
        WHERE doc_type = ? AND doc_num = ?
        """
        query_params = (doc_type, doc_num)
        cur.execute(query_text, query_params)
        row = cur.fetchone()

        return int(row["num"])


    except sqlite3.Error as err:
        raise IOError(f"getting transaction: {str(err)}") from err
    finally:
        con.close()


# post

def post(db_id: str, tra: Transaction) -> int | None:
    """ insert one transaction

    Args:
        tra (Transaction): Object containing the transaction data without num

    Returns:
        int: num of the inserted transaction
    """

    con, cur = dbutil.get_connection(db_id)

    try:
        query_text: str = """
        INSERT INTO transaction1
        (dt, descr)
        VALUES (?, ?);
        """

        query_params = (
            dateutil.date_iso_to_timestamp(tra.date),
            tra.descr)
        cur.execute(query_text, query_params)

        last_num = cur.lastrowid

        query_text = """
        INSERT INTO transaction1_detail
        (num, seq, account_num, val, dc, doc_type, doc_num)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        query_data = [(
            last_num,
            k + 1,
            seq.account,
            seq.val,
            seq.dc,
            seq.doc.type,
            seq.doc.num
            ) for (k, seq) in enumerate(tra.seqs, )]

        cur.executemany(query_text, query_data)

        con.commit()

        return last_num

    except sqlite3.Error as err:
        raise IOError(f"Error creating transaction: {str(err)}") from err
    finally:
        con.close()


def put(db_id: str, tra: Transaction):
    """ update one transaction

    Args:
        tra (Transaction): Object containing the new data of the transaction

    Returns:
        int: num of the updated transaction
    """

    con, cur = dbutil.get_connection(db_id)

    try:

        query_text = """
        UPDATE transaction1 SET
            dt = ?,
            descr = ?
        WHERE num = ?;
        """

        query_params = (
            dateutil.date_iso_to_timestamp(tra.date),
            tra.descr,
            tra.num)
        cur.execute(query_text, query_params)

        cur.execute(f"DELETE FROM transaction1_detail WHERE num = {tra.num};")

        query_text = """
        INSERT INTO transaction1_detail
        (num, seq, account_num, val, dc, doc_type, doc_num)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        query_data = [(
            tra.num,
            k + 1,
            seq.account,
            seq.val,
            seq.dc,
            seq.doc.type,
            seq.doc.num
            ) for (k, seq) in enumerate(tra.seqs)]
        cur.executemany(query_text, query_data)

        con.commit()

        return tra.num

    except sqlite3.Error as err:
        raise IOError(f"Error updating transaction {tra.num}: {str(err)}") from err
    finally:
        con.close()


def delete(db_id: str, num: int) -> int:
    """ Insert one transaction

    Args:
        num (int): number of the transaction to be deleted

    Returns:
        int: num of the deleted transaction
    """

    con, cur = dbutil.get_connection(db_id)

    try:
        cur.execute(f"DELETE FROM transaction1_detail WHERE num = {num};")
        con.commit()

        return num

    except sqlite3.Error as err:
        raise IOError(f"Error deleting transaction {num}: {str(err)}") from err
    finally:
        con.close()


def reset(db_id: str) -> None:
    """ reset transaction table """

    con, cur = dbutil.get_connection(db_id)

    try:
        with open(
            "ledger1/dao/csv/transaction1.csv",
            "r",
            encoding="UTF-8"
        ) as csvfile:

            reader = csv.DictReader(csvfile)
            for row in reader:
                cur.execute(
                    """
                    INSERT INTO transaction1 (num, dt, descr)
                        VALUES (?, ?, ?);
                    """,
                    (
                        int(row["num"]),
                        dateutil.date_iso_to_timestamp(row["dt"]),
                        str(row["descr"])
                    )
                )
                con.commit()

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
                        dc,
                        doc_type,
                        doc_num
                    ) VALUES (?, ?, ?, ?, ?, ?, ?);
                    """,
                    (
                        int(row["num"]),
                        int(row["seq"]),
                        str(row["account_num"]),
                        float(row["val"]),
                        row["dc"] == "True",
                        str(row["doc_type"]),
                        str(row["doc_num"]),
                    )
                )
                con.commit()

    except sqlite3.Error as err:
        raise IOError(f"Error resetting transaction: {str(err)}") from err
    finally:
        con.close()
