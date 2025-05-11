
from channels.db import database_sync_to_async
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError


@database_sync_to_async
def get_totem_infos(totem_id):
    from pages.models import Totem

    try:
        numeric_id = totem_id.split('_')[1]
        totem = Totem.objects.select_related("parking__zone").get(identity_code=numeric_id)
        # if totem.secret_token != secret_token:
            # return {"type": "error", "error": "Invalid secret token."} 
        price_list = [int(num) for num in totem.parking.zone.prices.split(',')]
        durations_list = [int(num) for num in totem.parking.zone.durations.split(',')]

        return {
            "type": "totem_data",
            "parking_name": totem.parking.address,
            "durations": durations_list,
            "prices": price_list,
        }

    except IndexError:
        return {"type": "error", "error": "Invalid totem_id format."}
    except Totem.DoesNotExist:
        return {"type": "error", "error": "Totem not found."}
    except Exception as e:
        return {"type": "error", "error": f"Server error: {str(e)}"}
#-----------------------------------------------------------------------------------
@database_sync_to_async
def get_user_cars(username):
    from pages.models import Car, User_developed, User

    try:
        user = User.objects.get(username=username)
        
        user_developed = User_developed.objects.get(user=user)
        
        cars = Car.objects.filter(user=user_developed)
        
        plates = [car.plate_number for car in cars]
        
        return ({
            "type": "user_cars",
            "plates": plates
        })
        
    except User.DoesNotExist:
        return {"type": "error", "error": "user does not exist."}
    except User_developed.DoesNotExist:
        return {"type": "error", "error": "user does not exist."}
    except Exception as e:
        return {"type": "error", "error": f"Server error: {str(e)}"}

# #--------------------------------------------------------------------------------------------------
@database_sync_to_async
def new_ticket(duration, price, totem_id,secret_token, plate):
    from pages.models import Totem, Car, Totem, Ticket
    
    try:
        totem_pk = int(totem_id.split('_')[1])
        
        totem = Totem.objects.get(identity_code=totem_pk)
        if totem.secret_token != secret_token:
            return {"type": "error", "error": "Invalid secret token."}        
        car, created = Car.objects.get_or_create(plate_number=plate.upper())

        try:
            price = float(price) 
        except ValueError:
            return {"type": "error", "error": "Invalid price format."}           
        ticket = Ticket.objects.create(
            duration=duration,
            price=price,
            totem=totem,
            car=car,
            payment_done=False
        )
        print("Ticket created successfully")
        
        return ({
            "type": "ticket_creation",
            "status": "success",
        })
    
    except ObjectDoesNotExist:
        print("Totem not found")
        return {"type": "error", "error": "totem does not exist."}

    except IntegrityError:
        print("Totem not found")
        return {"type": "error", "error": "Integrity error: possible duplicate entry"}

    except Exception as e:
        print("An unexpected error occurred")        
        return {"type": "error", "error": f"Server error: {str(e)}"}


#--------------------------------------------------------------------------------------------------

@database_sync_to_async

def get_car_parking_status(plate):
    from pages.models import Ticket, Car

    try:
        
        car= Car.objects.get(plate_number=plate.upper())

        # Get the most recent valid ticket for this car
        latest_ticket = Ticket.objects.filter(
            car=car,
        ).order_by('-start_time').first()

        if latest_ticket:
            # Calculate minutes remaining
            expiration_time = latest_ticket.start_time + timezone.timedelta(minutes=latest_ticket.duration)
            time_left = max(0, (expiration_time - timezone.now()).total_seconds() // 60)
            print(int(time_left))

            print("ticket found")   
            
            return ({
                "type": "get_car_parcking_status",
                "payment_done": latest_ticket.payment_done,
                "time_left": int(time_left)
            })
        
        else:
            return {"type": "error", "error": "no active ticket found."}
    except Car.DoesNotExist:
        print("Car not found")
        return {"type": "error", "error": "car does not exist."}


    except Exception as e:
        print("Handle any unexpected errors")
        return {"type": "error", "error": f"Server error: {str(e)}"}
    

# #--------------------------------------------------------------------------------------------------

@database_sync_to_async

def pay_ticket(ticket_id):
    from pages.models import  Ticket

    try:
        ticket = Ticket.objects.get(id=ticket_id)
        
        ticket.payment_done = True
        ticket.save()
        print("Ticket payment updated successfully")
        return ({
            "type": "pay_ticket",
            "status": "success",
        })

    except Ticket.DoesNotExist:
        print("Ticket not found")
        return ({
            "type": "pay_ticket",
            "status": "failed",
        })
    
    except Exception as e:
        print("Handle any unexpected errors")
        return {"type": "error", "error": f"Server error: {str(e)}"}
    