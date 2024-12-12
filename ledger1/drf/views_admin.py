""" reset DRF view

resets ledger1 db on the path ledger/reset

Arguments:
    request (Request): DRF REST request object

Returns:
    Response: DRF REST response reset confirmation
"""

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ledger1.admin import admin

@api_view(["GET", "POST"])
def view(request: Request, param: str = "", record_id: str = None):
    try:
        if request.method == "GET":
            ret: dict = admin.get(param, record_id)
        elif request.method == "POST":
            ret: dict = admin.post(param, data=request.data)
        else:
            raise ValueError("invalid method")

        status_code = ret.pop("status_code")
        response: Response = Response(ret)
        response.status_code = status_code
        return response

    except ValueError as err:
        res: Response = Response({ "message": f"Error: {str(err)}"})
        res.status_code = 400
        return res

    except Exception as err: # pylint: disable=broad-exception-caught
        res: Response = Response({ "message": f"Error: {str(err)}" })
        res.status_code = 500
        return res
