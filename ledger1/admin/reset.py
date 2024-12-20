from ledger1.dao.sqlite import dao
from ledger1.dao.sqlite import dao_account1
from ledger1.dao.sqlite import dao_document_type
from ledger1.dao.sqlite import dao_transaction1
from ledger1.dao.sqlite import dao_document
from ledger1.dao.sqlite import dao_setting
from ledger1.dao.sqlite import dao_document_field
from ledger1.dao.sqlite import dao_aux
from ledger1.admin.user import User
from ledger1.utils import fileio


def reset() -> None:
    """ Resets the sqlite3 database

    The order or the calls is important to establish the relations
    """

    settings: dict = fileio.get_file_settings()
    dao.reset(settings["file"]["sql"]["reset"])
    dao_document_type.reset()
    dao_account1.restore()
    dao_transaction1.reset()
    dao_document.restore(settings["file"]["csv"]["document"])
    dao_document_field.restore(settings["file"]["csv"]["document_field"])
    dao_setting.restore(settings["file"]["csv"]["setting"])
    dao_aux.restore(
        table_name="user",
        file_name=settings["file"]["csv"]["user"],
        db_format=User.get_db_format())
