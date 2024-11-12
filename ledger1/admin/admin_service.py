""" admin """

from ledger1.utils import fileio

from ledger1.dao.sqlite import dao
from ledger1.dao.sqlite import dao_account1
from ledger1.dao.sqlite import dao_document_type
from ledger1.dao.sqlite import dao_transaction1
from ledger1.dao.sqlite import dao_invoice2
from ledger1.dao.sqlite import dao_document


def reset() -> dict:
    """ Resets the sqlite3 database

    The order or the calls is important to establish the relations

    Returns:
       response
    """

    settings: dict = get_settings()

    dao.reset(settings["file"]["sql"]["reset"])
    dao_document_type.reset()
    dao_account1.reset()
    dao_transaction1.reset()
    dao_invoice2.restore(settings)
    dao_document.restore(settings["file"]["csv"]["document"])

    return {
        "code": 200,
        "message": "reset ok"
    }


def get_settings() -> dict:
    settings = fileio.read_json("./ledger1/settings.json")

    return settings
