from ledger1.dao.sqlite import dao_aux
from ledger1.admin.user import User

def get(user_id: int):
    table_name = "user"
    if user_id is None:
        data: list[dict] = dao_aux.get_many(table_name)
    else:
        db_data: dict = dao_aux.get_one(table_name, user_id)

        user: User = User()
        user.set_from_db(db_data)
        data = user.get_to_response()

    return data


def get_by_field(field_name: str, field_value: str | int):

    data: dict = dao_aux.get_by_field("user", field_name,  field_value)

    return data
