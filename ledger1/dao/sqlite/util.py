""" helpers for sqlite3 access """

import sqlite3

def get_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Connect to the db

    Returns:
        tuple: sqlite3 connection and cursor objects
    """

    con = sqlite3.connect("ledger1/dao/sqlite/tws.sqlite3")
    cur = con.cursor()
    return con, cur
