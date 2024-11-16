from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ledger1.document import payments

@api_view(["GET", "POST", "PUT", "DELETE"])
def view(request: Request, num: str = None):
    try:
        if request.method == "GET":
            ret: dict = payments.get(doc_dc=False, doc_type="eft", doc_num=num)

        elif request.method == "DELETE":
            ret = payments.delete(doc_type="eft", doc_num=num)

        elif request.method == "POST":
            ret = payments.post(data=request.data)

        # elif request.method == "PUT":

        #     ret = invoices2.put(data=request.data)

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
        print(str(err))
        res.status_code = 500
        return res
