#from rest_framework.response import Response
#from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from .models import Totem,User_developed,Car,Ticket
from django.contrib.auth.models import User 
import json
from django.db import transaction


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
    
    


#--------------------------------------------------------------------------------------------------
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError

def new_ticket(duration, price, totem_id, plate):
    try:
        totem_pk = int(totem_id.split('_')[1])
        
        totem = Totem.objects.get(identity_code=totem_pk)
        
        car, created = Car.objects.get_or_create(plate_number=plate.upper())
                    
        ticket = Ticket.objects.create(
            duration=duration,
            price=price,
            totem=totem,
            car=car,
            payment_done=False
        )
        print("Ticket created successfully")
        print(ticket.pk)
        return JsonResponse({"status": "success"})
    
    
    except (ValidationError, ValueError, IndexError):
        print("Invalid input data")
        return JsonResponse({"status": "failed"}, status=400)

    except ObjectDoesNotExist:
        print("Totem or car not found")
        return JsonResponse({"status": "failed"}, status=404)

    except IntegrityError:
        print("Integrity error: possible duplicate entry")
        return JsonResponse({"status": "failed"}, status=500)

    except Exception:
        print("An unexpected error occurred")
        return JsonResponse({"status": "failed"}, status=500)
    

#--------------------------------------------------------------------------------------------------

from django.utils import timezone
from .models import Ticket

def get_car_parking_status(plate):
    try:
        
        car= Car.objects.get(plate_number=plate.upper())

        # Get the most recent valid ticket for this car
        latest_ticket = Ticket.objects.filter(
            car=car,
            payment_done=True,

        ).order_by('-start_time').first()

        if latest_ticket:
            # Calculate minutes remaining
            expiration_time = latest_ticket.start_time + timezone.timedelta(minutes=latest_ticket.duration)
            time_left = max(0, (expiration_time - timezone.now()).total_seconds() // 60)
            print(int(time_left))
            print("ticket found")
            return JsonResponse({"time_left": int(time_left)})
        
        else:
            print("No ticket found")
            return JsonResponse({"time_left": 0})

    except Exception:
        print("Handle any unexpected errors")
        return JsonResponse({"time_left": 0})
    

#--------------------------------------------------------------------------------------------------
def pay_ticket(ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        
        ticket.payment_done = True
        ticket.save()
        print("Ticket payment updated successfully")
        return JsonResponse({"status": "success"})
    
    except Ticket.DoesNotExist:
        print("Ticket not found")
        return JsonResponse({"status": "failed"})
    
    except Exception:
        print("An unexpected error occurred")
        return JsonResponse({"status": "failed"})