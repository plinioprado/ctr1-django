from ledger1.dao.sqlite import dao_aux

def get(user_id: int):
    table_name = "user"
    if id is None:
        data: list[dict] = dao_aux.get_many(table_name)
    else:
        data: dict = dao_aux.get_one(table_name, user_id)

    return data


def get_by_field(field_name: str, field_value: str | int):
    users = [
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "pass": "12345",
            "entities": ["example"],
            "entity": "example",
        },
        {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "pass": "12345",
            "entities": ["example"],
            "entity": "example",
        }
    ]

    user = [user for user in users if user[field_name] == field_value]

    return {} if user == [] else user[0]

