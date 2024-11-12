import sqlite3
from ledger1.utils.fileio import read_text

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


def reset(file_name: str) -> None:
    """ Reset blank ledger1 tables """

    print(file_name)

    try:

        query_text: str = read_text(file_name)

        con, cur = get_connection()
        cur.executescript(query_text)
        con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"reseting account {str(err)}") from err
    except Exception as err:
        raise err
    finally:
        con.close()
