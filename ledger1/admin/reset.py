
from ledger1.admin import settings as settings_service

from ledger1.dao.sqlite import dao
from ledger1.dao.sqlite import dao_account1
from ledger1.dao.sqlite import dao_document_type
from ledger1.dao.sqlite import dao_transaction1
from ledger1.dao.sqlite import dao_document
from ledger1.dao.sqlite import dao_setting
from ledger1.dao.sqlite import dao_document_field


def reset() -> None:
    """ Resets the sqlite3 database

    The order or the calls is important to establish the relations
    """

    settings: dict = settings_service.get_file_settings()
    dao.reset(settings["file"]["sql"]["reset"])
    dao_document_type.reset()
    dao_account1.reset()
    dao_transaction1.reset()
    dao_document.restore(settings["file"]["csv"]["document"])
    dao_document_field.restore(settings["file"]["csv"]["document_field"])
    dao_setting.restore(settings["file"]["csv"]["setting"])

    print(9)
