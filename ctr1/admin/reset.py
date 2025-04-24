from ctr1.dao.sqlite import dao
from ctr1.dao.sqlite import dao_setting
from ctr1.dao.sqlite import dao_aux
from ctr1.admin.user import User
from ctr1.utils import fileio


def reset(db_id) -> None:
    """ Resets the sqlite3 database

    The order or the calls is important to establish the relations
    """

    settings_file: dict = fileio.get_file_settings()
    dao.reset(db_id, settings_file["file"]["sql"]["reset"])
    dao_setting.restore(db_id, settings_file["file"]["csv"]["setting"])
    dao_aux.restore(
        db_id=db_id,
        table_name="user",
        file_name=settings_file["file"]["csv"]["user"],
        db_format=User.get_db_format())
