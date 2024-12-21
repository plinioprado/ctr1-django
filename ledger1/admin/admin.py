""" admin

This is the component that will get the requests from outside the appplicaiton
and return the requests

 """

from ledger1.admin import reset as reset_service
from ledger1.admin import session
from ledger1.admin import auxs
from ledger1.admin.aux import Aux
from ledger1.utils import fileio


def login(data: dict) -> dict:
    try:
        if sorted(data.keys()) != ["entity", "user_email", "user_pass"]:
            raise ValueError("400")

        user: dict = auxs.get_by_field(field_name="email", field_value=data["user_email"])

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


def get(param: str, query: dict | None = None, record_id: str | None = None) -> dict:
    settings_data = fileio.get_file_settings()
    file_format_path = settings_data["file"]["format"]

    # because the query values in Django came as an array
    filters: dict = {name: query[name][0] for name in query} if query else {}

    if param in ["user", "setting"]:
        obj: Aux = auxs.get_object(param)

        if record_id is None:
            data: list[dict] | dict = auxs.get_many(obj, filters)
            data_format: dict = fileio.read_json(f"{file_format_path}/{param}s_format.json")
            data_filters: list[dict] | None = auxs.get_filters(data_format, filters)

            response = {
                "data": data,
                "filters": data_filters,
                "format": data_format,
                "message": "ok",
                "status_code": 200
            }

        else:
            data = auxs.get_one(record_id, obj)
            data_format = fileio.read_json(f"{file_format_path}/{param}_format.json")

            response = {
                "data": data,
                "format": data_format,
                "message": "ok",
                "status_code": 200
            }


    elif param == "reset":
        reset()

        response = {
        "status_code": 200,
        "message": "reset ok"
    }
    else:
        raise ValueError(f"invalid param {param}")

    return response


def post(param: str, data: dict) -> dict:
    if param in ["user", "setting"]:
        obj: Aux = auxs.get_object(param)
        record_id = auxs.post(data, obj)

    else:
        raise ValueError(f"invalid param {param}")

    return {
        "status_code": 200,
        "message": f"{param} {record_id} created",
        "data": {
            obj.primary_key_form: record_id
        }
    }


def put(param: str, data: dict) -> dict:

    if param in ["user", "setting"]:
        obj: Aux = auxs.get_object(param)
        record_id = auxs.put(data, obj)

    else:
        raise ValueError(f"invalid param {param}")

    return {
        "status_code": 200,
        "message": f"{param} {record_id} updated",
        "data": {
            obj.primary_key_form: record_id
        }
    }


def delete(param: str, record_id: str) -> dict:

    if param in ["user", "setting"]:
        obj: Aux = auxs.get_object(param)
        record_id = auxs.delete(record_id, obj)

    else:
        raise ValueError(f"invalid param {param}")

    return {
        "status_code": 200,
        "message": f"{param} {record_id} deleted",
        "data": {
            obj.primary_key_form: record_id
        }
    }


def reset() -> None:
    reset_service.reset()


def get_db_settings(key: str) -> dict:
    settings_list: list[dict] = auxs.get_db_settings(key)

    settings_dict: dict = {setting["key"]: setting["value"] for setting in settings_list}

    return settings_dict
