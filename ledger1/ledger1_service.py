""" contains the function run, that redirects the user requests to the various services """

from ledger1.reports.reports_service import service
from ledger1.util.dbutil import reset_db


def run(op: str) -> dict:
    """ Redirects the user requests to the various services

    Args:
        op: name of the servide requested by the user

    Returns:
        dict ready to be serialized as a REST response
    """

    try:

        if op.startswith("reports/"):
            data: dict = service(op.replace("reports/", ""))
            response = {
                "code": 200,
                "message": "ok",
                "data": data
            }
        elif op == "reset_db":
            message: str = reset_db()
            response = {
                "code": 200,
                "message": message,
            }
        else:
            response = {"message": "invalid option"}

    except Exception as err: # pylint: disable=broad-exception-caught
        return { "code": 500, "message": str(err) }

    return response
