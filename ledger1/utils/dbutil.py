""" database utilities """
import sqlite3
from ledger1.utils import fileio


def get_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Connect to the db and

    Returns:
        Tuple with sqlite3 connection and cursor objects
    """

    settings = fileio.read_json("./ledger1/settings.json")
    dbfilename = settings["sqlite3"]["file_db"]

    con = sqlite3.connect(dbfilename, timeout=10)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return con, cur
