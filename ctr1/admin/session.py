

def get_session(api_key: str, entity_name: str, db_settings: list[dict], user: dict):

    menu_options = get_menu_options(db_settings)

    session = {
        "user": {
            "api_key": api_key,
            "name": user["name"],
        },
        "entity": {
            "name": entity_name,
        },
        "menu_options": menu_options,
    }

    return session


def get_menu_options(db_settings: list[dict]) -> list[dict]:
    menu_options = []

    for setting in db_settings:
        if setting["key"].startswith("menu_"):
            menu_options.append(setting)

    return menu_options
