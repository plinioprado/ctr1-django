from ledger1.dao.sqlite import dao_aux
from ledger1.admin.user import User


def get_many(obj: object):
    db_data: list[dict] = dao_aux.get_many(obj.table_name)

    data = []
    for row in db_data:
        obj.set_from_db(row)
        data.append(obj.get_to_response_list())

    return data


def get_one(record_id: str, obj: object):

    if record_id == "new":
        data = obj.get_to_response_new()

    else:
        db_data: dict = dao_aux.get_one(obj.table_name, record_id)

        obj.set_from_db(db_data)
        data = obj.get_to_response()

    return data


def post(data: dict, obj: object):
    obj.set_from_request(data)
    db_data = User.get_db_format()
    record_id = dao_aux.post(
        table_name=obj.table_name,
        data=obj.get_to_db(),
        db_format=db_data)

    return record_id


def put(data: dict, obj: object):
    obj.set_from_request(data)
    db_data = User.get_db_format()
    user_id = dao_aux.put(
        table_name=obj.table_name,
        data=obj.get_to_db(),
        db_format=db_data)

    return user_id


def delete(param: str, record_id: str):
    user_id = dao_aux.delete(
        table_name=param,
        record_id=record_id)

    return user_id


def get_by_field(field_name: str, field_value: str | int):

    data: dict = dao_aux.get_by_field("user", field_name,  field_value)

    return data
