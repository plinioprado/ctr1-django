""" reset db """

from ledger1.dao.sqlite.account1_dao import reset as reset_account
from ledger1.dao.sqlite.transaction1_dao import reset as reset_transaction


def reset() -> None:
    """ reset all tables """

    reset_account()
    reset_transaction()
