""" responses for calls to /documents/admin"""

from documents.util import fileutil
from documents.dao.sqlite import dao_admin
from documents.dao.sqlite import dao_invoice2

def service(op: str) -> dict:

    if op == "reset":
        response: dict = resetdb()
    else:
        raise ValueError("invalid document admin option")

    return response


def resetdb() -> dict:
    settings = get_settings()

    dao_admin.resetdb(settings)
    dao_invoice2.restore(settings)

    return {
        "code": 200,
        "message": "reset ok"
    }


def get_settings() -> dict:
    settings = fileutil.read_json("./documents/settings.json")

    return settings
