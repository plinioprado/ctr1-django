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

        user: dict = users.get_by_email(data["user_email"])

        if not user or data["user_pass"] != user["pass"] or data["entity"] not in user["entities"]:
            raise ValueError("401")

        api_key: str = "1q2w3e4r5t6y7u8i9o0p"
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


def reset() -> dict:
    reset_service.reset()

    return {
        "code": 200,
        "message": "reset ok"
    }
