""" report DRF view
Receives a REST request from .urls and responds with data from the ledger1.report component

Arguments:
    request (Request): DRF REST request object

Returns:
    Response: DRF REST response with ledger1 data

"""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ledger1.reports_service import service

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view(request: Request, name: str):

    try:
        if request.method == "GET":

            data: dict = service(
                name,
                acc=request.query_params.get("acc"),
                acc_to=request.query_params.get("acc_to"),
                date=request.query_params.get("date"),
                date_to=request.query_params.get("date_to")
            )

            response: Response = Response({
                "message": "ok",
                "data": data
            })
            response.status_code = 200

        else:
            raise ValueError("invalid method")

    except ValueError as err:
        response: Response = Response({"message": f"Error: {str(err)}"})
        response.status_code = 400

    except Exception as err: # pylint: disable=broad-exception-caught
        response: Response = Response({ "message": f"Error: {str(err)}" })
        response.status_code = 500

    return response
