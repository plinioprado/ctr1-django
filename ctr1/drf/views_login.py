from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ctr1.admin import admin
from ctr1.utils.error_client import ClientError

@api_view(["POST"])
def view(request: Request):
    try:
        if request.method == "POST":
            ret: dict = admin.login(request.data)
        else:
            raise ValueError("invalid method")

        status_code = ret.pop("status_code")
        response: Response = Response(ret)
        response.status_code = status_code
        return response

    except ClientError as err:
        res: Response = Response({ "message": err.message})
        res.status_code = err.status_code
        return res

    except ValueError as err:
        res = Response({ "message": str(err) })
        res.status_code = 400
        return res

    except Exception as err: # pylint: disable=broad-exception-caught
        res = Response({ "message": str(err) })
        res.status_code = 500
        return res
