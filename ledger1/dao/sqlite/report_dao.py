""" Data access objects for chart of accounts report to sqlite """

import datetime
from ledger1.dao.sqlite.util import get_connection
from ledger1.models.account1 import Account1


def get() -> list[Account1]:
    """
    Read (get) all accounts

    Returns:
        List of all accounts as a list of Accounts
    """

    report_rows = []
    con, _ = get_connection()
    for row in con.execute("SELECT num, name, dc FROM account1"):
        account = Account1(num=str(row[0]), name=str(row[1]), dc=int(row[2]) == 1)
        report_rows.append(account)

    return report_rows


def get_general_ledger(
    date_from: str,
    date_to: str
) -> list[dict]:
    """
    data for general ledger
    """

    report_rows = []
    con, _ = get_connection()

    for row in con.execute(
        """
        SELECT
            td.account_num,
            acc.name as account_name,
            t.dt,
            td.num,
            t.descr,
            t.doc_type,
            t.doc_num,
            td.seq,
            td.val,
            td.dc
        FROM transaction1_detail td
            INNER JOIN transaction1 t ON td.num = t.num
            INNER JOIN account1 acc ON acc.num = td.account_num
        WHERE t.dt BETWEEN ? AND ?
        ORDER BY td.account_num, t.dt, t.num, td.seq
        """,
        (
            datetime.datetime.fromisoformat(date_from).timestamp(),
            datetime.datetime.fromisoformat(date_to).timestamp()
        )
    ):

        report_rows.append({
            "account_num": str(row[0]),
            "account_name": str(row[1]),
            "dt": datetime.datetime.fromtimestamp(row[2]).isoformat()[0:10],
            "num": int(row[3]),
            "descr": str(row[4]),
            "doc_type": str(row[5]),
            "doc_num": int(row[6]),
            "seq": int(row[7]),
            "val": float(row[8]),
            "dc": bool(row[9])
        })

    return report_rows


def get_journal(
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
    con, _ = get_connection()

    for row in con.execute(
        """
        SELECT
            t.dt,
            td.num,
            t.descr,
            t.doc_type,
            t.doc_num,
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
            "doc_num": int(row[4]),
            "seq": int(row[5]),
            "acc_num": str(row[6]),
            "acc_name": str(row[7]),
            "val": float(row[8]),
            "dc": "D" if row[9] else "C",
        })

    return report_rows


def get_trial_balance(
    date_from: str,
    date_to: str
) -> list[dict]:
    """
    data for general ledger
    """

    con, _ = get_connection() # pylint: disable=unused-variable

    # get rows from db
    dao_rows = []
    for row in con.execute("""
        SELECT
            acc.num AS acc_num,
            acc.name AS acc_name,
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
        ORDER BY acc_num
        """,
        (
            datetime.datetime.fromisoformat(date_from).timestamp(),
            datetime.datetime.fromisoformat(date_to).timestamp(),
            datetime.datetime.fromisoformat(date_from).timestamp(),
            datetime.datetime.fromisoformat(date_to).timestamp(),
        )):

        val_db = 0 if row[2] is None else row[2]
        val_cr = 0 if row[3] is None else row[3]

        dao_rows.append({
            "acc_num": str(row[0]),
            "acc_name": str(row[1]),
            "val_db": val_db,
            "val_cr": val_cr,
            "val_bal": val_db + val_cr
            })

        # compute total by level
        l1_db = 0
        l1_cr = 0
        l2_db = 0
        l2_cr = 0

        rows: list[dict] = []
        for dao_row in reversed(dao_rows):
            level = len(dao_row["acc_num"].replace(".0", "").split("."))
            acc_num = dao_row["acc_num"]
            acc_name = dao_row["acc_name"]
            if level == 3:
                val_db = dao_row["val_db"]
                val_cr = dao_row["val_cr"]
                l2_db += val_db
                l2_cr += val_cr
                l1_db += val_db
                l1_cr += val_cr
            elif level == 2:
                val_db = l2_db
                val_cr = l2_cr
                l2_db = 0
                l2_cr = 0
            elif level == 1:
                val_db = l1_db
                val_cr = l1_cr
                l1_db = 0
                l1_cr = 0
            else:
                val_db = 0
                val_cr = 0

            rows.append({
                "acc_num": acc_num,
                "acc_name": acc_name,
                "val_db": val_db,
                "val_cr": val_cr,
                "val_bal": val_db + val_cr
            })

    data: list[dict] = list(reversed(rows))

    return data
