from ledger1.utils import fileio
from ledger1.dao.sqlite import dao_setting


def get(record_id: str,  query: dict) -> dict:
    if record_id is None:
        data = dao_setting.get_many(query)
    else:
        data = dao_setting.get_one(record_id)

    return data


def get_file_settings() -> dict:
    settings = fileio.read_json("./ledger1/settings.json")

    return settings


def get_db_settings(key: str) -> dict:
    data: list[dict] = dao_setting.get_many(key)
    return data
