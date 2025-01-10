""" reset DRF view

resets ledger1 db on the path ledger/reset

Arguments:
    request (Request): DRF REST request object

Returns:
    Response: DRF REST response reset confirmation
"""

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view #, permission_classes
# from rest_framework.permissions import IsAuthenticated
from ledger1.document import documents

@api_view(["GET", "POST", "PUT", "DELETE"])
# @permission_classes([IsAuthenticated])
def view(request: Request, num: str = None):
    try:
        api_key: str = request.headers["Authorization"]

        if request.method == "GET":
            ret: dict = documents.get(
                api_key,
                doc_dc=request.query_params.get("dc") == 'true',
                doc_type="inv2",
                doc_num=num)

        elif request.method == "POST":
            ret = documents.post(api_key, data=request.data)

        elif request.method == "PUT":

            ret = documents.put(api_key, data=request.data)

        elif request.method == "DELETE":
            ret = documents.delete(
                api_key,
                doc_type="inv2",
                doc_num=num)

        else:
            raise ValueError("invalid method")

        status_code = ret.pop("status")
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
