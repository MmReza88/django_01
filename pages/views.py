#from rest_framework.response import Response
#from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from .models import Totem,User_developed,Car,Ticket
from django.contrib.auth.models import User 
import json
from django.db import transaction

'''
@require_GET
def get_totem_infos(request, totem_id):
    return JsonResponse(apiFuntions.getTotem)
'''
def get_user_cars(request, username):
    pass
#--------------------------------------------------------------------------------------------------

def new_ticket(duration, price, totem_id, plate):
    pass
#--------------------------------------------------------------------------------------------------
def get_car_parking_status(plate):
    pass
#--------------------------------------------------------------------------------------------------
def pay_ticket(ticket_id):
    pass