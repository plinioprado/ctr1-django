""" account DRF view
Receives a REST request from .urls and responds with data from the ledger1.account component

Arguments:
    request (Request): DRF REST request object

Returns:
    Response: DRF REST response with ledger1 data

"""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view #, permission_classes
# from rest_framework.permissions import IsAuthenticated
from ledger1.account import accounts

@api_view(["GET", "POST", "PUT", "DELETE"])
# @permission_classes([IsAuthenticated])
def view(request: Request, acc: str | None = None):

    try:
        api_key: str = request.headers["Authorization"]

        if request.method == "GET":

            ret: dict = accounts.get(api_key, acc)

        elif request.method == "POST":

            ret = accounts.post(api_key, request.data)

        elif request.method == "PUT":

            ret = accounts.put(api_key, data=request.data)

        elif request.method == "DELETE":

            ret = accounts.delete(api_key, acc_num=acc)

        else:
            raise ValueError("invalid method")

        status_code = ret.pop("code")
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
