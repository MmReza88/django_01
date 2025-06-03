
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
@database_sync_to_async#
def new_ticket(duration, price, totem_id,secret_token, plate , card_number):
    from pages.models import Totem, Car, Totem, Ticket , Card , Parking
    
    try:
        totem_pk = int(totem_id.split('_')[1])
    
    except (IndexError, ValueError):
        print("Invalid totem_id format")           
        return {"type": "error", "error": "Invalid totem_id format."}
    
    try:
        totem = Totem.objects.get(identity_code=totem_pk)
    except Totem.DoesNotExist:
        print("Totem not found")           
        return {"type": "error", "error": "totem does not exist."}
    
    if totem.secret_token != secret_token:
        print("Invalid secret token")
        return {"type": "error", "error": "Invalid secret token."} 
    
    Parking = totem.parking
    if Parking is None:
        print("Parking not found")           
        return {"type": "error", "error": "Parking not found."}
    
    car, created = Car.objects.get_or_create(plate_number=plate.upper())
           
    try:
        price = float(price) 
    except ValueError:
        return {"type": "error", "error": "Invalid price format."}           
    try:
        duration = int(duration)
    except ValueError:
        return {"type": "error", "error": "Invalid duration format."}    
    try:
        card = Card.objects.get(card_number=card_number)
    except Card.DoesNotExist:
        print("Card not found")           
        return {"type": "error", "error": "card does not exist."}



    try:
        ticket_qs=Ticket.objects.filter(
            car=car,
            Parking=Parking,
            stop_time__gt=timezone.now()
        )
        
        if ticket_qs.exists():
            ticket = ticket_qs.first()  
            ticket.stop_time += timezone.timedelta(minutes=duration)  
            ticket.save()  # Save the changes
            print("active Ticket found")
            print("Ticket updated with new stop_time")
            return ({
                    "type": "ticket_update",
                    "status": "success",
                })
        else:
            print("No active ticket found")
            # Create a new ticket
            
            ticket = Ticket.objects.create(
                #duration=duration,
                stop_time=timezone.now() + timezone.timedelta(minutes=duration),
                price=price,
                #totem=totem,
                Parking=Parking,
                car=car,
                card_number=card_number,
                )
            print("Ticket created successfully")
            return ({
                    "type": "ticket_creation",
                    "status": "success",
                })   
    except Exception as e:
        print("Handle any unexpected errors")
        return {"type": "error", "error": f"Server error: {str(e)}"}
    
#--------------------------------------------------------------------------------------------------
@database_sync_to_async
def get_car_parking_status(plate):
    from pages.models import Ticket, Car

    try: 
        car= Car.objects.get(plate_number=plate.upper())
    except Car.DoesNotExist:
        print("Car not found")
        return ({
                "type": "get_car_parcking_status",
                "time_left": int(0),
                "end_time":  None,

            })

    try:
        latest_ticket = Ticket.objects.filter(
            car=car,
        ).order_by('-start_time').first()

        if latest_ticket:
            time_left = max(0, (latest_ticket.stop_time - timezone.now()).total_seconds() // 60)            
            print("Ticket found")
            print("Time left in minutes:", time_left)
            return ({
                "type": "get_car_parcking_status",
                "time_left": int(time_left),
                "end_time": latest_ticket.stop_time.strftime("%Y-%m-%d %H:%M:%S"),
            })
        else:
            print("No active ticket found")
            return ({
                "type": "get_car_parcking_status",
                "time_left": int(0),
                "end_time":  None,

            })

    except Exception as e:
        print("Handle any unexpected errors")
        return {"type": "error", "error": f"Server error: {str(e)}"}
    

# #--------------------------------------------------------------------------------------------------
