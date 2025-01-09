""" Data access objects for chart of accounts report to sqlite """

import datetime
from ledger1.utils import dbutil
from ledger1.account.account1 import Account1


def get(
        db_id: str,
        acc_from: str,
        acc_to: str
    ) -> list[Account1]:
    """
    Read (get) all accounts

    Params:
        acc_from (str): account number from in format 9.9.9
        acc_to (str): account number fo in format 9.9.9

    Returns:
        List of all accounts as a list of Accounts
    """

    con, _ = dbutil.get_connection(db_id)

    report_rows = []
    for row in con.execute("""
        SELECT num, name, dc FROM account1
        WHERE (num BETWEEN ? AND ?)
        """,
        (acc_from, acc_to)):
        account = Account1(num=str(row[0]), name=str(row[1]), dc=bool(row[2]) == 1)
        report_rows.append(account)

    return report_rows


def get_general_ledger(
    db_id: str,
    date_from: str,
    date_to: str,
    acc_from: str,
    acc_to: str,
) -> list[dict]:
    """
    data for general ledger
    """

    con, _ = dbutil.get_connection(db_id)

    report_rows = []
    for row in con.execute(
        """
            SELECT
                td.account_num,
                acc.name as account_name,
                ? AS dt,
                0 AS num,
                "opening balance" AS descr,
                "" AS doc_type,
                "" AS doc_num,
                0 AS seq,
                SUM(IIF(td.dc = 1, td.val, -td.val)) AS val,
                1 AS dc
            FROM transaction1_detail td
                INNER JOIN transaction1 t ON td.num = t.num
                INNER JOIN account1 acc ON acc.num = td.account_num
            WHERE t.dt < ?
            GROUP BY td.account_num

        UNION
            SELECT
                td.account_num,
                acc.name as account_name,
                t.dt,
                t.num,
                t.descr,
                td.doc_type,
                td.doc_num,
                td.seq,
                td.val,
                td.dc
            FROM transaction1_detail td
                INNER JOIN transaction1 t ON td.num = t.num
                INNER JOIN account1 acc ON acc.num = td.account_num
            WHERE (account_num BETWEEN ? AND ?) AND (t.dt BETWEEN ? AND ?)
        ORDER BY td.account_num, t.dt, t.num, td.seq
        """,
        (
            datetime.datetime.fromisoformat(date_from).timestamp(),
            datetime.datetime.fromisoformat(date_from).timestamp(),
            acc_from,
            acc_to,
            datetime.datetime.fromisoformat(date_from).timestamp(),
            datetime.datetime.fromisoformat(date_to).timestamp(),
        )
    ):

        report_rows.append({
            "account_num": str(row["account_num"]),
            "account_name": str(row["account_name"]),
            "dt": datetime.datetime.fromtimestamp(row["dt"]).isoformat()[0:10],
            "num": int(row["num"]),
            "descr": str(row["descr"]),
            "doc_type": str(row["doc_type"]),
            "doc_num": str(row["doc_num"]),
            "seq": int(row["seq"]),
            "val": 0 if row["val"] is None else float(row["val"]),
            "dc": bool(row["dc"] == 1)
        })

    return report_rows


def get_journal(
        db_id: str,
        date_from: str,
        date_to: str
    ) -> list[dict]:
    """
    Read (get) the transaction rows for a journal report

    Params:
        date_from = initial date in yyyy-mm-dd format
        date_to = final date in yyyy-mm-dd format
    Returns:
        List of journal rows as dict
    """

    report_rows = []
    con, _ = dbutil.get_connection(db_id)

    for row in con.execute(
        """
        SELECT
            t.dt,
            td.num,
            t.descr,
            td.doc_type,
            td.doc_num,
            td.seq,
            td.account_num,
            acc.name as account_name,
            td.val,
            td.dc
        FROM transaction1_detail td
            INNER JOIN transaction1 t ON td.num = t.num
            INNER JOIN account1 acc ON acc.num = td.account_num
        WHERE t.dt BETWEEN ? AND ?
        ORDER BY t.dt, t.num, td.seq
        """,
        (
            datetime.datetime.fromisoformat(date_from).timestamp(),
            datetime.datetime.fromisoformat(date_to).timestamp()
        )
    ):
        report_rows.append({
            "dt": datetime.datetime.fromtimestamp(row[0]).isoformat()[0:10],
            "num": int(row[1]),
            "descr": str(row[2]),
            "doc_type": str(row[3]),
            "doc_num": str(row[4]),
            "seq": int(row[5]),
            "acc_num": str(row[6]),
            "acc_name": str(row[7]),
            "val": float(row[8]),
            "dc": "D" if row[9] else "C",
        })

    return report_rows


def get_trial_balance(
    db_id: str,
    date_from: str,
    date_to: str,
    acc_from: str,
    acc_to: str,
) -> list[dict]:
    """
    data for general ledger
    """

    con, _ = dbutil.get_connection(db_id) # pylint: disable=unused-variable

    # get rows from db
    dao_rows = []
    for row in con.execute("""
        SELECT
            acc.num AS acc_num,
            acc.name AS acc_name,
            (
                SELECT SUM(IIF(td.dc == 1, td.val, -td.val))
                FROM transaction1_detail td
                    INNER JOIN transaction1 t ON t.num = td.num
                WHERE td.account_num = acc.num
                    AND t.dt < ?
            ) AS val_open,
            (
                SELECT SUM(td.val)
                FROM transaction1_detail td
                    INNER JOIN transaction1 t ON t.num = td.num
                WHERE td.account_num = acc.num AND td.dc
                    AND t.dt BETWEEN ? AND ?
                ORDER BY td.account_num
            ) AS val_db,
            (
                SELECT - SUM(td.val)
                FROM transaction1_detail td
                    INNER JOIN transaction1 t ON t.num = td.num
                WHERE td.account_num = acc.num AND NOT td.dc
                    AND t.dt BETWEEN ? AND ?
                ORDER BY td.account_num
            ) AS val_cr
        FROM account1 acc
        WHERE (acc_num BETWEEN ? AND ?)
        ORDER BY acc_num
        """,
        (
            datetime.datetime.fromisoformat(date_from).timestamp(),
            datetime.datetime.fromisoformat(date_from).timestamp(),
            datetime.datetime.fromisoformat(date_to).timestamp(),
            datetime.datetime.fromisoformat(date_from).timestamp(),
            datetime.datetime.fromisoformat(date_to).timestamp(),
            acc_from,
            acc_to
    )):

        val_open = 0 if row["val_open"] is None else float(row["val_open"])
        val_db = 0 if row["val_db"] is None else float(row["val_db"])
        val_cr = 0 if row["val_cr"] is None else float(row["val_cr"])

        dao_rows.append({
            "acc_num": str(row["acc_num"]),
            "acc_name": str(row["acc_name"]),
            "val_open": val_open,
            "val_db": val_db,
            "val_cr": val_cr,
            "val_bal": val_db + val_cr
            })

        # compute total by level
        l1_open = 0
        l1_db = 0
        l1_cr = 0
        l2_open = 0
        l2_db = 0
        l2_cr = 0

        # reversed to better total the upper depths
        rows: list[dict] = []
        for dao_row in reversed(dao_rows):
            level = len(dao_row["acc_num"].replace(".0", "").split("."))
            acc_num = dao_row["acc_num"]
            acc_name = dao_row["acc_name"]
            if level == 3:
                val_open = dao_row["val_open"]
                val_db = dao_row["val_db"]
                val_cr = dao_row["val_cr"]
                l2_open += val_open
                l2_db += val_db
                l2_cr += val_cr
                l1_open += val_open
                l1_db += val_db
                l1_cr += val_cr
            elif level == 2:
                val_open = l2_open
                val_db = l2_db
                val_cr = l2_cr
                l2_open = 0
                l2_db = 0
                l2_cr = 0
            elif level == 1:
                val_open = l1_open
                val_db = l1_db
                val_cr = l1_cr
                l1_open = 0
                l1_db = 0
                l1_cr = 0
            else:
                val_open = 0
                val_db = 0
                val_cr = 0

            rows.append({
                "acc_num": acc_num,
                "acc_name": acc_name,
                "val_open": val_open,
                "val_db": val_db,
                "val_cr": val_cr,
                "val_bal": val_db + val_cr
            })

    data: list[dict] = list(reversed(rows))

    return data


def get_documents(
    db_id: str,
    date_from: str,
    date_to: str,
    doc_type: str
) -> list[dict]:
    """
    data documents report
    """

    con, cur = dbutil.get_connection(db_id) # pylint: disable=unused-variable

    query_text = """
    SELECT
        td.doc_num,
        t.dt,
        t.descr,
        CONCAT(td.num, ".", td.seq) AS tra,
        CONCAT(td.account_num, " ", a.name) AS account,
        td.val,
        td.dc
    FROM transaction1_detail td
        INNER JOIN transaction1 t ON t.num = td.num
        INNER JOIN account1 a ON a.num = td.account_num
    WHERE t.dt BETWEEN ? AND ? AND td.doc_type = ?
    ORDER BY td.doc_num, t.dt, td.num, td.seq
    """
    query_params = (
        datetime.datetime.fromisoformat(date_from).timestamp(),
        datetime.datetime.fromisoformat(date_to).timestamp(),
        doc_type
    )
    cur.execute(query_text, query_params)

    rows = [["num","date","transaction","account","history","val_db","val_cr"]]
    for record in cur.fetchall():
        val_db = record["val"] if record["dc"] else 0
        val_cr = record["val"] if not record["dc"] else 0

        rows.append([
            record["doc_num"],
            datetime.datetime.fromtimestamp(record["dt"]).isoformat()[0:10],
            record["descr"],
            record["tra"],
            record["account"],
            val_db,
            val_cr
            ])

    return rows
