from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from invoice1.invoice1_service import Invoice1Service as service

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def invoice1(request: Request, num: int):

    if request.method == "GET":

        res = service.get_by_num(num)
        return Response(res)

    return Response({'message': 'invalid method'})
