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
from ledger1.reports.reports_service import service

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view(request: Request):
    if request.method == "GET":
        res = {
            "code": 200,
            "message": "account wip"
        }
        return Response(res)

    return Response({'message': 'invalid method'})
