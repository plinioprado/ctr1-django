""" admin """

from ledger1.dao.sqlite import dao_account1
from ledger1.dao.sqlite import dao_document_type
from ledger1.dao.sqlite import dao_transaction1


def reset() -> dict:
    """ Resets the sqlite3 database

    The order or the calls is important to establish the relations

    Returns:
       response
    """

    dao_document_type.reset()
    dao_account1.reset()
    dao_transaction1.reset()


    return {
        "code": 200,
        "message": "reset ok"
    }
