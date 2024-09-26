from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from invoice1.invoice1_service import Invoice1Service as service

@api_view(["GET","POST","PUT","DELETE"])
@permission_classes([IsAuthenticated])
def invoice1(request: Request):

    if request.method == "GET":
        res = service.get()
        return Response(res)

    if request.method == "POST":
        res = service.post(request.data)
        return Response(res)

    if request.method == "PUT":
        res = service.put(request.data)
        return Response(res)

    if request.method == "DELETE":
        res = service.delete(request.data)
        return Response(res)

    return Response({'message': 'invalid method'})
