from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Totem

@api_view(["GET"])
def get_totem_infos(request, totem_id):
    totem = Totem.objects.get(id=totem_id)
    
    data = {"parking_name": totem.parking.name, "durations": totem.get_durations(), "prices": totem.get_prices()}
    return Response(data)