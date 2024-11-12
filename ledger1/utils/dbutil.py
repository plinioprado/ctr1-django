""" database utilities """
from ledger1.utils import fileio
import sqlite3
from ledger1.dao.sqlite.dao_transaction1 import reset as reset_transaction
from ledger1.dao.sqlite.dao_account1 import reset as reset_account

def reset_db() -> str:
    """ Resets the sqlite3 database

    Returns:
       'message ok' if no error
    """

    reset_account()
    reset_transaction()

    return "reset ok"


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
