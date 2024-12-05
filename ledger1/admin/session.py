

def get_session(user: dict, entity: str, api_key: str):

    session = {
        "user": {
            "api_key": api_key,
            "name": user["name"],
            "entity": entity,
        }
    }

    return session
