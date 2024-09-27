""" invoice1 DRF view
Receives a REST request from ./urls and responds with data from the ledger1.account1 component

Arguments:
    request (Request): DRF REST request object

Returns:
    Response: DRF REST response with ledger1 data

"""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import ledger1.transactions1 as service

@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def view(request: Request):

    try:

        if request.method == "GET":

            num = request.query_params.get("num")

            res = service.get(num)

        elif request.method == "POST":

            res: dict = service.post(request.data)

        elif request.method == "PUT":

            res: dict = service.put(request.data)

        elif request.method == "DELETE":

            num = request.query_params.get("num")

            res: dict = service.delete(num)

        else:
            raise ValueError("invalid method")

    except ValueError as err:
        res = {
            "code": 400,
            "message": f"Error: {str(err)}",
        }
    except Exception as err: # pylint: disable=broad-exception-caught
        res = {
            "code": 500,
            "message": f"Error: {str(err)}",
        }

    return Response(res)
