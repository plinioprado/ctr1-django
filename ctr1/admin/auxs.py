""" This module """

from ctr1.dao.sqlite import dao_aux
from ctr1.admin.user import User
from ctr1.admin.setting import Setting
from ctr1.admin.aux import Aux


def get_many(obj: Aux, filters: dict, db_id: str) -> list[dict]:
    db_data: list[dict] = dao_aux.get_many(obj=obj, filters=filters, db_id=db_id)

    data: list[dict] = []
    for row in db_data:
        obj.set_from_db(row)
        data.append(obj.get_to_response_list())

    return data


def get_one(record_id: str, obj: Aux, db_id: str) -> dict:
    if record_id == "new":
        data = obj.get_to_response_new()

    else:
        db_data: dict = dao_aux.get_one(obj, record_id, db_id)

        obj.set_from_db(db_data)
        data = obj.get_to_response()

    return data


def post(data: dict, obj: Aux, db_id: str) -> str:
    obj.set_from_request(data)
    record_id = dao_aux.post(obj, db_id)

    return str(record_id)


def put(data: dict, obj: Aux, db_id: str) -> str:
    obj.set_from_request(data)
    record_id = dao_aux.put(obj, db_id)

    return str(record_id)


def delete(record_id: str, obj: Aux, db_id: str) -> str:
    result_id = dao_aux.delete(record_id, obj, db_id)

    return str(result_id)


def get_by_field(db_id: str, field_name: str, field_value: str | int) -> dict:
    data: dict = dao_aux.get_by_field(db_id, "user", field_name, field_value)

    return data


def get_filters(data_format: dict, filters: dict | None) -> list[dict]:

    if "filters" not in data_format.keys():
        return []

    data: list[dict] = []
    for data_filter in data_format["filters"]:
        value = filters["name"] if (filters is not None and "name" in filters.keys()) else None
        data.append({
            data_filter["name"]: value
        })

    return data


def get_object(resource: str) -> Aux:
    if resource == "user":
        obj: Aux = User()
    elif resource == "setting":
        obj = Setting()
    else:
        raise ValueError(f"invalid resource {resource}")

    return obj


def get_db_settings(key: str, db_id: str) -> list[dict]:
    data: list[dict] = get_many(
        obj=Setting(),
        filters={"key": key},
        db_id=db_id
    )

    return data
