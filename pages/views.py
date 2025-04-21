#from rest_framework.response import Response
#from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Totem,User_developed,Car
from django.contrib.auth.models import User 
@require_GET
def get_totem_infos(request, totem_id):
    try:
        numeric_id = totem_id.split('_')[1]
        totem = Totem.objects.get(identity_code=numeric_id)
        
        # Convert prices and durations to lists
        price_list = [int(num) for num in totem.parking.zone.prices.split(',')]
        durations_list = [int(num) for num in totem.parking.zone.durations.split(',')]

        return JsonResponse({
            "parking_name": totem.parking.address,
            "durations": durations_list,  # Now a list, not a string
            "prices": price_list,
        })

    except IndexError:
        return JsonResponse({"error": "Invalid totem_id format."}, status=400)
    except Totem.DoesNotExist:
        return JsonResponse({"error": "Totem not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)
    

def get_user_cars(request, username):
    try:
       
        user = User.objects.get(username=username)
        
        
        user_developed = User_developed.objects.get(user=user)
        
        
        cars = Car.objects.filter(user=user_developed)
        
       
        plates = [car.plate_number for car in cars]
        
        return JsonResponse({
            "plates": plates
        })
        
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except User_developed.DoesNotExist:
        return JsonResponse({"error": "User profile not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)