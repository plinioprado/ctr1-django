

def get_session(api_key: str, entity_name: str, user: dict):

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
