import sqlite3
from documents.util import fileio


def resetdb() -> None:
    settings = fileio.read_json("/document/settings.json")


def get_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Connect to the db and

    Returns:
        Tuple with sqlite3 connection and cursor objects
    """

    con = sqlite3.connect("ledger1/dao/sqlite/tws.sqlite3")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return con, cur
