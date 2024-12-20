from ledger1.admin import auxs
from ledger1.admin.setting import Setting


def get_db_settings(key: str):
    data = auxs.get_many(
        obj=Setting(),
        filters={"key": key}
    )

    return data
