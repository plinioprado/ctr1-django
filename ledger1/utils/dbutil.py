""" database utilities """

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
