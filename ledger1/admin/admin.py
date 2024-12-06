""" admin

This is the component that will get the requests from outside the appplicaiton
and return the requests

 """

from ledger1.admin import reset as reset_service
from ledger1.admin import session
from ledger1.admin import users

def login(data: dict):
    try:

        if sorted(data.keys()) != ["entity", "user_email", "user_pass"]:
            raise ValueError("400")

        user: dict = users.get_by_field(field_name="email", field_value=data["user_email"])

        if (not user or
            data["user_pass"] != user["password"] or
            data["entity"] not in user["entities"]):

            raise ValueError("401")

        api_key: str = user["api_key"]
        data = session.get_session(user, data["entity"], api_key)

        response = {
            "data": data,
            "message": "ok",
            "status_code": 200,
        }

        return response

    except ValueError as err:
        return {
            "message": "invalid login",
            "status_code": int(str(err))
        }


def get(param: str, record_id: int = None):
    if param == "user":
        response = get_user(record_id)
    elif param == "reset":
        response = reset()
    else:
        raise ValueError(f"invalid param {param}")

    return response


def get_user(record_id: int):
    data = users.get(record_id)

    return {
        "data": data,
        "message": "ok",
        "status_code": 200
    }


def reset() -> dict:
    reset_service.reset()

    return {
        "status_code": 200,
        "message": "reset ok"
    }
