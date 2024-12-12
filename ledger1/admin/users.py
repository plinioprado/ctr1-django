from ledger1.dao.sqlite import dao_aux
from ledger1.admin.user import User

def get(user_id: str):
    table_name = "user"
    user: User = User()
    if user_id is None:
        db_data: list[dict] = dao_aux.get_many(table_name)

        data = []
        for usr in db_data:
            user.set_from_db(usr)
            data.append(user.get_to_response_list())

    else:
        db_data: dict = dao_aux.get_one(table_name, user_id)

        user.set_from_db(db_data)
        data = user.get_to_response()

    return data


def post(param: str, data: dict):
    user: User = User()
    user.set_from_request(data)
    db_data = User.get_db_format()
    user_id = dao_aux.post(
        table_name=param,
        data=user.get_to_db(),
        db_format=db_data)

    return user_id


def get_by_field(field_name: str, field_value: str | int):

    data: dict = dao_aux.get_by_field("user", field_name,  field_value)

    return data
