from ledger1.utils import fileio
from ledger1.dao.sqlite import dao_setting


def get() -> dict:
    print("will get settings")
    data = dao_setting.get_many()
    return data


def get_file_settings() -> dict:
    settings = fileio.read_json("./ledger1/settings.json")

    return settings


def get_db_settings(key: str) -> dict:
    data: list[dict] = dao_setting.get_many(key)
    return data
