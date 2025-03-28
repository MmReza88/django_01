from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def get_totem_infos(request, totem_id):
    print(totem_id)
    data = {"message": "Hello, DRF!"}
    return Response(data)