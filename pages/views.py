from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import park_auth.api_functions as api
from pages.models import Totem
from pages.models import Ticket
from pages.models import Service_provider
from django.shortcuts import render
from qrcode.constants import ERROR_CORRECT_L


import qrcode
import base64
from io import BytesIO
from django.urls import reverse


@api_view(['GET']) 
def start_card(request, totem_id, secret_token, card_info):
    
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
                "type": "send_start",
                "card": card_info,
            }
        )
    except Exception as e:
        print(f"Error: {e}")
        return Response({"type": "error", "error": "Something is not good"})
    
    return Response({"type": "start", "secret_token": secret_token, "card_info": card_info})

# #--------------------------------------------------------------------------------------------------

@api_view(['GET']) 
def get_totem_infos(request, totem_id , secret_token):   
    return Response(async_to_sync(api.get_totem_infos)(totem_id, secret_token))
# #--------------------------------------------------------------------------------------------------
@api_view(['GET']) 
def  get_user_cars(request, username):   
    return Response(async_to_sync(api.get_user_cars)(username))
# #--------------------------------------------------------------------------------------------------
@api_view(['GET']) 
def new_ticket(request,duration, price, totem_id, secret_token, plate, card_number):
    return Response(async_to_sync(api.new_ticket)(duration, price, totem_id, secret_token, plate,  card_number))
#     
#     pass
# #--------------------------------------------------------------------------------------------------
@api_view(['GET']) 
def get_car_parking_status(request,plate):
    return Response(async_to_sync(api.get_car_parking_status)(plate))

# #--------------------------------------------------------------------------------------------------
def ticket_view(request, ticket_id):
    try:
        ticket =Ticket.objects.get(id=ticket_id)
        message = f"Ticket ID: {ticket.id}"

        # Generate absolute URL for the ticket page
        ticket_url = request.build_absolute_uri(
            reverse('ticket view', args=[ticket_id])
        )

        
        # Generate QR code with the URL
        qr = qrcode.QRCode(
        version=1,  # controls the size: 1 is smallest (21x21 modules)
        error_correction=ERROR_CORRECT_L,
        box_size=4,  # default is 10; smaller means smaller QR pixels
        border=2,    # default is 4; smaller border reduces overall size
        )

        qr.add_data(ticket_url) 
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        return render(request, 'ticket_detail.html', {
            'ticket': ticket,
           # 'qr_code': qr_base64,
            'ticket_url': ticket_url
        })





        #return HttpResponse(message, content_type='text/plain')
    except Ticket.DoesNotExist:
        #return HttpResponse("Ticket not found.", status=404)
        return render(request, 'ticket_detail.html', {'error': 'Ticket not found.'}, status=404)
    except Exception as e:
        #return HttpResponse(f"Server error: {str(e)}", status=500) 
        return render(request, 'ticket_detail.html', {'error': f'Server error: {str(e)}'}, status=500)


# #--------------------------------------------------------------------------------------------------
@api_view(['GET'])
def get_user_for_badge(request, badge_number):
    return Response(async_to_sync(api.get_user_for_badge)(badge_number))
# #--------------------------------------------------------------------------------------------------
@api_view(['GET'])
def get_all_info_car(request, plate , service_provider):
    return Response(async_to_sync(api.get_all_info_car)(plate, service_provider))


#--------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def get_all_parkings(request):
    return Response(async_to_sync(api.get_all_parkings)())

@api_view(["GET"])
def get_parking_infos(request, parking_name):
    return Response(async_to_sync(api.get_parking_infos)(parking_name))
    