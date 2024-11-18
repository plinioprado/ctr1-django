""" Test Util functions """

import sqlite3
import ledger1.utils.field as field
from ledger1.utils import dbutil


def test_date_iso_is_valid():
    assert field.date_iso_is_valid("2020-01-02")
    assert not field.date_iso_is_valid("2020-02-30")


def test_acc_num_is_valid():
    assert field.acc_num_is_valid("1.1.1")
    assert not field.acc_num_is_valid("1.1.11")
    assert not field.acc_num_is_valid("x.x.x")


def get_last_tra_num():
    con, cur = dbutil.get_connection()

    try:
        query_text = """
        SELECT num
        FROM Transaction1
        ORDER BY num DESC
        LIMIT 1;
        """
        cur.execute(query_text)
        con.commit()

        row = cur.fetchone()

        print(111, dict(row))

        return row["num"]

    except sqlite3.DatabaseError as err:
        raise IOError(f"finding last transaction: {str(err)}") from err
    finally:
        con.close()
