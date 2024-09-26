""" report DRF view
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
from ledger1.reports.reports_service import service

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view(request: Request, name: str):
    if request.method == "GET":
        try:

            data: dict = service(name)

            res = {
                "code": 200,
                "message": "ok",
                "data": data
            }
        except Exception as err:
            res = {
                "code": 500,
                "message": f"Error: {str(err)}",
            }

        return Response(res)

    return Response({'message': 'invalid method'})
