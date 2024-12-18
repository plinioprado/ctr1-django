""" admin

This is the component that will get the requests from outside the appplicaiton
and return the requests

 """

from ledger1.admin import reset as reset_service
from ledger1.admin import session
from ledger1.admin import settings
from ledger1.admin import users
from ledger1.admin.user import User
from ledger1.utils import fileio

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


def get(param: str, filters: dict = None, record_id: str = None):
    settings_data = fileio.get_file_settings()
    obj = User()
    file_format_path = settings_data["file"]["format"]

    if param == "user":
        if record_id is None:
            data: list[dict] = users.get_many(obj)
            data_format: dict = fileio.read_json(f"{file_format_path}/users_format.json")

        else:
            data: dict = users.get_one(record_id, obj)
            data_format = fileio.read_json(f"{file_format_path}/user_format.json")

        response = {
            "data": data,
            "format": data_format,
            "message": "ok",
            "status_code": 200
        }

    elif param == "setting":
        if record_id is None:
            data: list[dict] | dict = settings.get_many(filters)
            data_format = fileio.read_json(f"{file_format_path}/settings_format.json")

        else:
            data = settings.get_one(record_id)
            data_format = fileio.read_json(f"{file_format_path}/setting_format.json")

        response = {
            "data": data,
            "filters": filters,
            "format": data_format,
            "message": "ok",
            "status_code": 200
        }


    elif param == "reset":
        reset_service.reset()

        response = {
        "status_code": 200,
        "message": "reset ok"
    }
    else:
        raise ValueError(f"invalid param {param}")

    return response


def post(param: str, data: dict):
    if param == "user":
        obj: User = User()
        record_id = users.post(data, obj)

    else:
        raise ValueError(f"invalid param {param}")

    return {
        "status_code": 200,
        "message": f"{param} {record_id} created",
        "data": {
            "id": record_id
        }
    }


def put(param: str, data: dict):

    if param == "user":
        obj: User = User()
        record_id = users.put(data, obj)

    else:
        raise ValueError(f"invalid param {param}")

    return {
        "status_code": 200,
        "message": f"{param} {record_id} updated",
        "data": {
            "id": record_id
        }
    }


def delete(param: str, record_id: str = None):
    record_id = users.delete(param, record_id)
    return {
        "status_code": 200,
        "message": f"{param} {record_id} deleted",
        "data": {
            "id": record_id
        }
    }
