
import sqlite3
from documents.util import fileutil


def executescript(query_text) -> None:
    """ Execute query """

    con, cur = get_connection()
    try:
        cur.executescript(query_text)
        with con:
            con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"reseting account {str(err)}") from err
    except Exception as err:
        raise err
    finally:
        con.close()


def get_connection() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Connect to the db and

    Returns:
        Tuple with sqlite3 connection and cursor objects
    """

    settings = fileutil.read_json("./documents/settings.json")
    dbfilename = settings["sqlite3"]["file_db"]

    con = sqlite3.connect(dbfilename, timeout=10)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return con, cur
