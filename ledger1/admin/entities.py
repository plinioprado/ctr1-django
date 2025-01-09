"""
This component handles the entities

Summary:

* User log in providing email, pass and the entity he want to access.
* The login will return in the session:
  * api_key to inform the back-end what entity us being accessed
  * entity name to be shown in the front-end footer
* Every request contains the api_key and it redirects to the correspondent db

* api_key has 2 parts: entity and user: "xxxxxx-xxxxxxxxxxxxxxxxxxx"

Initially, all entities will be in a sqlite db therefore the connectin data will be just a path
"""

from ledger1.utils import fileio


def get_db_id_by_api_key(api_key: str) -> dict:

    entity_key: str = api_key.replace("Bearer ", "").split("-")[0]
    api_key: dict = get_entity("key", entity_key)["id"]

    return api_key


def get_entity(field: str, value: str) -> dict:

    settings_data = fileio.get_file_settings()
    entities = settings_data["entities"]
    entity: dict = [en for en in entities if en[field] ==  value][0]

    return entity

