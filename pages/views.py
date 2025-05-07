from rest_framework.response import Response
from rest_framework.decorators import api_view
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import park_auth.api_functions as api
from pages.models import Car, User_developed, User,Totem

@api_view(['GET']) 
def start_card(request, totem_id, secret_token, card_info):
    
    #TODO: Check it the secret_token is valid for the totem_id
    try:
        numeric_id = totem_id.split('_')[1]
        totem = Totem.objects.select_related("parking__zone").get(identity_code=numeric_id)
        print(f"Totem: {totem}")
        print(f"Totem id: nu")
        if totem.secret_token != secret_token:
            return Response({"type": "error", "error": "Invalid secret token."})
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            totem_id,
            {
                "type": "send_start",  # this matches a method name in your consumer
            }
        )
    except Exception as e:
        print(f"Error: {e}")
        return Response({"type": "error", "error": "Something is not good"})
    
    return Response({"type": "start", "secret_token": secret_token, "card_info": card_info})


# @api_view(['GET']) 
# def get_totem_infos(request, totem_id):
#     return Response(api.get_totem_infos(totem_id))
# #--------------------------------------------------------------------------------------------------

# def new_ticket(duration, price, totem_id, plate):
#     pass
# #--------------------------------------------------------------------------------------------------
# def get_car_parking_status(plate):
#     pass
# #--------------------------------------------------------------------------------------------------
# def pay_ticket(ticket_id):
#     pass