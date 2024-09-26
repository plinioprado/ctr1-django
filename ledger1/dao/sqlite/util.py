""" helpers for sqlite3 access """

import sqlite3
import datetime
import math

def get_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Connect to the db

    Returns:
        tuple: sqlite3 connection and cursor objects
    """

    con = sqlite3.connect("ledger1/dao/sqlite/tws.sqlite3")
    cur = con.cursor()
    return con, cur


def date_iso_to_timestamp(date_iso: str) -> int:
    """
    Convert date iso to timestamp through datetime to assure it is valid

    Arguments:
        date_iso (str): date in ISO yyyy-mm-dd

    Returns:
        int: date in unix timestamp
    """

    return math.floor(datetime.datetime.fromisoformat(date_iso).timestamp())


def date_timestamp_to_iso(date_ts: int) -> str:
    """
    Convert date iso to timestamp through datetime to assure it is valid

    Arguments:
        date_iso (str): date in ISO yyyy-mm-dd

    Returns:
        int: date in unix timestamp
    """

    return datetime.datetime.fromtimestamp(date_ts).isoformat()[0:10]
