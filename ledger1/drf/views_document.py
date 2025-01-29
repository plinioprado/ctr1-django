""" documents view

handles requests to path documents

Arguments:
    request (Request): DRF REST request object
    doc_type (str): document type
    doc_num (str optional): document number

Returns:
    Response: DRF REST response reset confirmation
"""

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ledger1.document import documents

@api_view(["GET", "POST", "PUT", "DELETE"])
def view(request: Request, doc_type: str = None, doc_num: str = None) -> Response:
    try:
        api_key: str = request.headers["Authorization"]
        doc_dc = request.query_params.get("dc") == 'true'

        if request.method == "GET":
            ret: dict = documents.get(
                api_key=api_key,
                doc_dc=doc_dc,
                doc_type=doc_type,
                doc_num=doc_num)

        elif request.method == "POST":
            ret = documents.post(
                api_key,
                doc_type=doc_type,
                data=request.data)

        elif request.method == "PUT":
            ret = documents.put(
                api_key,
                doc_type=doc_type,
                doc_num=doc_num,
                data=request.data)

        elif request.method == "DELETE":
            ret = documents.delete(
                api_key,
                doc_type=doc_type,
                doc_num=doc_num)

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
