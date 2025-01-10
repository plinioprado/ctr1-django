""" admin

This is the component that will get the requests from outside the appplicaiton
and return the requests

 """

from ledger1.admin import reset as reset_service
from ledger1.admin import session
from ledger1.admin import auxs
from ledger1.admin.aux import Aux
from ledger1.utils import fileio
from ledger1.admin import entities


def login(data: dict) -> dict:
    try:
        if sorted(data.keys()) != ["entity", "user_email", "user_pass"]:
            raise ValueError("400")

        # data from file settings
        entity_id = data["entity"]
        param_db_entity: str = entities.get_entity("id", entity_id)

        # data from user
        user: dict = auxs.get_by_field(
            db_id=param_db_entity["id"],
            field_name="email",
            field_value=data["user_email"]
        )

        if (not user or data["user_pass"] != user["password"]):
            raise ValueError("401")

        # data from db settings
        obj: Aux = auxs.get_object("setting")
        entity_name: dict = auxs.get_one("entity_name", obj, entity_id)["value"]

        api_key: str = f"{param_db_entity["key"]}-{user["api_key"]}"
        data = session.get_session(api_key, entity_name, user)

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


def get(
        api_key: str,
        param: str,
        query: dict | None = None,
        record_id: str | None = None
    ) -> dict:

    db_id: str = entities.get_db_id_by_api_key(api_key)

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
        raise ValueError(f"invalid param {param}")

    return response


def post(param: str, data: dict, api_key: str) -> dict:
    if param in ["user", "setting"]:
        db_id: str = entities.get_db_id_by_api_key(api_key)

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


def put(param: str, data: dict, api_key: str) -> dict:

    if param in ["user", "setting"]:
        db_id: str = entities.get_db_id_by_api_key(api_key)

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


def delete(param: str, record_id: str, api_key: str) -> dict:

    if param in ["user", "setting"]:
        db_id: str = entities.get_db_id_by_api_key(api_key)
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


def get_db_settings(key: str, db_id: str = "") -> dict:
    settings_list: list[dict] = auxs.get_db_settings(key, db_id)

    settings_dict: dict = {setting["key"]: setting["value"] for setting in settings_list}

    return settings_dict
