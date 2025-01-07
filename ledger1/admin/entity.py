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


def get_entity_key(entity_id: str) -> str:
    """
    called from the login and will return the api_key to be added to the session in the response
    """

    data: dict = _get_entity_data_by_id(entity_id)

    return data["key"]


def get_connection_data(api_key: str) -> dict:
    """
    called in each request to provide the connection data to the correspondent db
    Initially, just the path to a sqlite db
    """

    return {
        "path": "xxx"
    }


def _get_entity_data_by_id(entity_id) -> dict:

    settings_data = fileio.get_file_settings()
    entities = settings_data["entities"]
    entity: dict = [en for en in entities if en["id"] ==  entity_id][0]

    return entity
