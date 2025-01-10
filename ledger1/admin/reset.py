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


def reset(db_id) -> None:
    """ Resets the sqlite3 database

    The order or the calls is important to establish the relations
    """

    settings_file: dict = fileio.get_file_settings()
    dao.reset(db_id, settings_file["file"]["sql"]["reset"])
    dao_document_type.reset(db_id)
    dao_account1.restore(db_id)
    dao_transaction1.reset(db_id)
    dao_document.restore(db_id, settings_file["file"]["csv"]["document"])
    dao_document_field.restore(db_id, settings_file["file"]["csv"]["document_field"])
    dao_setting.restore(db_id, settings_file["file"]["csv"]["setting"])
    dao_aux.restore(
        db_id=db_id,
        table_name="user",
        file_name=settings_file["file"]["csv"]["user"],
        db_format=User.get_db_format())
