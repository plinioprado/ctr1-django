""" invoice1 DRF view
Receives a REST request from ./urls and responds with data from the ledger1.transaction component

Arguments:
    request (Request): DRF REST request object

Returns:
    Response: DRF REST response with ledger1 data

"""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view #, permission_classes
# from rest_framework.permissions import IsAuthenticated
import ledger1.transaction.transaction_service as service

@api_view(["GET", "POST", "PUT", "DELETE"])
# @permission_classes([IsAuthenticated])
def view(request: Request, num: int | None = None):

    try:

        if request.method == "GET":

            ret = service.get(
                num,
                date=request.query_params.get("date"),
                date_to=request.query_params.get("date_to"))

        elif request.method == "POST":

            ret: dict = service.post(request.data)

        elif request.method == "PUT":

            ret: dict = service.put(request.data)

        elif request.method == "DELETE":

            ret: dict = service.delete(num)

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

    return Response(res)
