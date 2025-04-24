""" admin

This is the component that will get the requests from outside the appplicaiton
and return the requests

 """

from ctr1.admin import reset as reset_service
from ctr1.admin import auxs
from ctr1.admin import entities
from ctr1.admin import session
from ctr1.admin.aux import Aux
from ctr1.utils import fileio
from ctr1.utils import errorutil


def login(data: dict) -> dict:
    try:
        if sorted(data.keys()) != ["entity", "user_email", "user_pass"]:
            errorutil.handle_error("invalid login data", 401)

        # data from file settings
        try:
            param_db_entity: str = entities.get_entity("id", data["entity"])
        except IndexError:
            errorutil.handle_error("invalid login", 401)

        # data from user
        user: dict = auxs.get_by_field(
            db_id=param_db_entity["id"],
            field_name="email",
            field_value=data["user_email"]
        )

        if (not user or data["user_pass"] != user["password"]):
            errorutil.handle_error("invalid login", 401)

        # data from db settings
        obj: Aux = auxs.get_object("setting")
        entity_name: dict = auxs.get_one("entity_name", obj, data["entity"])["value"]
        db_settings: list[dict] = auxs.get_many(obj, "", param_db_entity["id"])

        api_key: str = f"{param_db_entity['key']}-{user['api_key']}"
        data = session.get_session(api_key, entity_name, db_settings, user)

        response = {
            "data": data,
            "message": "ok",
            "status_code": 200,
        }

        return response

    except ValueError as err:
        return {
            "message": f"value error on login: {str(err)}",
            "status_code": 400
        }


# get


def get(
        api_key: str,
        param: str,
        query: dict | None = None,
        record_id: str | None = None
    ) -> dict:

    db_id: str = get_db_id_by_api_key(api_key)

    settings_data = fileio.get_file_settings()
    file_format_path = settings_data["file"]["format"]

    # because the query values in Django came as an array
    filters: dict = {name: query[name][0] for name in query} if query else {}

    if param in ["user", "setting"]:
        obj: Aux = auxs.get_object(param)

        if record_id is None:
            data: list[dict] | dict = auxs.get_many(obj, filters, db_id)
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
            data = auxs.get_one(record_id, obj, db_id)
            data_format = fileio.read_json(f"{file_format_path}/{param}_format.json")

            response = {
                "data": data,
                "format": data_format,
                "message": "ok",
                "status_code": 200
            }


    elif param == "reset":
        reset(db_id)

        response = {
        "status_code": 200,
        "message": "reset ok"
    }
    else:
        response = None
        errorutil.handle_error(f"invalid param {param}")


    return response


def get_db_id_by_api_key(api_key: str) -> str:

    entity_key: str = api_key.replace("Bearer ", "").split("-")[0]
    api_key = entities.get_entity("key", entity_key)["id"]

    return api_key


def get_db_settings(key: str, db_id: str = "") -> dict:
    settings_list: list[dict] = auxs.get_db_settings(key, db_id)

    settings_dict: dict = {setting["key"]: setting["value"] for setting in settings_list}

    return settings_dict


# post

def post(param: str, data: dict, api_key: str) -> dict:
    if param in ["user", "setting"]:
        db_id: str = get_db_id_by_api_key(api_key)

        obj: Aux = auxs.get_object(param)
        record_id = auxs.post(data, obj, db_id)

    else:
        raise ValueError(f"invalid param {param}")

    return {
        "status_code": 200,
        "message": f"{param} {record_id} created",
        "data": {
            obj.primary_key_form: record_id
        }
    }


# put

def put(param: str, data: dict, api_key: str) -> dict:

    if param in ["user", "setting"]:
        db_id: str = get_db_id_by_api_key(api_key)

        obj: Aux = auxs.get_object(param)
        record_id = auxs.put(data, obj, db_id)

    else:
        raise ValueError(f"invalid param {param}")

    return {
        "status_code": 200,
        "message": f"{param} {record_id} updated",
        "data": {
            obj.primary_key_form: record_id
        }
    }


# delete

def delete(param: str, record_id: str, api_key: str) -> dict:

    if param in ["user", "setting"]:
        db_id: str = get_db_id_by_api_key(api_key)
        obj: Aux = auxs.get_object(param)
        record_id = auxs.delete(record_id, obj, db_id)

    else:
        raise ValueError(f"invalid param {param}")

    return {
        "status_code": 200,
        "message": f"{param} {record_id} deleted",
        "data": {
            obj.primary_key_form: record_id
        }
    }


def reset(db_id) -> None:

    reset_service.reset(db_id)
