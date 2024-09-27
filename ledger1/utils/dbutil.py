""" database utilities """

import ledger1.dao.sqlite.reset_dao as reset_dao

def reset_db() -> str:
    """ Resets the sqlite3 database

    Returns:
       'message ok' if no error
    """

    reset_dao.reset()

    return "reset ok"
