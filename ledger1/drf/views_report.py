""" report DRF view
Receives a REST request from .urls and responds with data from the ledger1.report component

Arguments:
    request (Request): DRF REST request object

Returns:
    Response: DRF REST response with ledger1 data

"""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view #, permission_classes
# from rest_framework.permissions import IsAuthenticated
from ledger1.reports.reports_service import service

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def view(request: Request, name: str):

    try:
        auth_header: str = request.headers["Authorization"]
        if request.method == "GET":

            ret: dict = service(
                name,
                auth_header=auth_header,
                acc=request.query_params.get("acc"),
                acc_to=request.query_params.get("acc_to"),
                date=request.query_params.get("date"),
                date_to=request.query_params.get("date_to"),
                doc_type=request.query_params.get("doc_type")
            )

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
