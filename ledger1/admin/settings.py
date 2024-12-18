from ledger1.dao.sqlite import dao_setting


def get_many(filters: dict) -> list[dict]:
    data = dao_setting.get_many(filters)

    return data


def get_one(record_id: str) -> dict:
    data = dao_setting.get_one(record_id)

    return data


def get_db_settings(key: str) -> dict:
    data: list[dict] = dao_setting.get_many(key)

    return data
