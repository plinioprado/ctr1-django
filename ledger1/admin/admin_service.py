""" admin """

import ledger1.dao.sqlite.reset_dao as dao

def reset() -> dict:
    """ Resets the sqlite3 database

    Returns:
       'reset ok' if no error
    """

    dao.reset()

    return {
        "code": 200,
        "message": "reset ok"
    }
