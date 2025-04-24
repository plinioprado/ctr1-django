""" database utilities """
import sqlite3
from ctr1.utils import fileio


def get_connection(db_id: str = "") -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Connect to the db and

    Returns:
        Tuple with sqlite3 connection and cursor objects
    """

    settings = fileio.read_json("./ctr1/settings.json")
    db_id = "example" if db_id == "" else db_id

    dbfilename = [s for s in settings["entities"] if s["id"] == db_id][0]["path"]

    con = sqlite3.connect(dbfilename, timeout=10)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return con, cur
