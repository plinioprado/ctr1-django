import sqlite3
from ctr1.utils import dbutil
from ctr1.utils.fileio import read_text

def reset(db_id: str, file_name: str) -> None:
    """ Reset blank ledger1 tables """

    con, cur = dbutil.get_connection(db_id)

    try:
        query_text: str = read_text(file_name)
        cur.executescript(query_text)
        con.commit()

    except sqlite3.DatabaseError as err:
        raise ValueError(f"reseting account {str(err)}") from err
    except Exception as err:
        raise err
    finally:
        con.close()
