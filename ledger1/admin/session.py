

def get_session(entity_name: str, user: dict, api_key: str):

    session = {
        "user": {
            "api_key": api_key,
            "name": user["name"],
        },
        "entity": {
            "name": entity_name,
        }
    }

    return session
