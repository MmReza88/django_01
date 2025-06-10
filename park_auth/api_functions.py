
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
def new_ticket(duration, price, totem_id, secret_token, plate, card_number):
    from pages.models import Totem, Car, Ticket
    from django.utils import timezone

    try:
        totem_pk = int(totem_id.split('_')[1])
    except (IndexError, ValueError):
        return {"type": "error", "error": "Invalid totem_id format."}

    try:
        totem = Totem.objects.get(identity_code=totem_pk)
    except Totem.DoesNotExist:
        return {"type": "error", "error": "Totem does not exist."}

    if totem.secret_token != secret_token:
        return {"type": "error", "error": "Invalid secret token."}

    Parking = totem.parking
    if Parking is None:
        return {"type": "error", "error": "Parking not found."}

    car, _ = Car.objects.get_or_create(plate_number=plate.upper())

    try:
        price = float(price)
    except ValueError:
        return {"type": "error", "error": "Invalid price format."}

    try:
        duration = int(duration)
    except ValueError:
        return {"type": "error", "error": "Invalid duration format."}

    try:
        # Get the last ticket for this car and parking, regardless of active/inactive
        last_ticket = Ticket.objects.filter(
            car=car,
            Parking=Parking
        ).order_by('-stop_time').first()
    
        # Determine base time
        now = timezone.now()
        last_stop_time = now

        if last_ticket:
            last_stop_time = max(last_ticket.stop_time, now)

        # Build the new ticket start/stop time
        new_start_time = last_stop_time
        new_stop_time = new_start_time + timezone.timedelta(minutes=duration)
        Ticket.objects.create(
            start_time=new_start_time,
            stop_time=new_stop_time,
            price=price,
            Parking=Parking,
            car=car,
            card_number=card_number,
        )
        last_ticket = Ticket.objects.filter(
            car=car,
            Parking=Parking
        ).order_by('-stop_time').first()

        return {
            "type": "ticket_creation",
            "status": "success",
            "ticket_id": str(last_ticket.id),
            "start_time": int(last_ticket.start_time.timestamp()),
            "stop_time": int(last_ticket.stop_time.timestamp()),
        }

    except Exception as e:
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

@database_sync_to_async
def get_user_for_badge(badge_number):
    from pages.models import Badge, User

    try:
        badge = Badge.objects.get(badge_number=badge_number)
    except Badge.DoesNotExist:
        return {"type": "error", "error": "No controller has been assigned for this badge."}
    try:
        user = badge.user
       
        if not user:
            return {"type": "error", "error": "User not found for the given badge."}
        
        return {
            "username": user.username,
            "service_provider": badge.Service_provider.name if Badge.Service_provider else None,
        }
    except Exception as e:
        return {"type": "error", "error": f"Server error: {str(e)}"}
#
# #--------------------------------------------------------------------------------------------------
# TODO: add the parking name in the response
@database_sync_to_async
def get_all_info_car(plate , service_provider):
    from pages.models import Car, User_developed, Fine, Chalk, Ticket ,Service_provider
    from django.utils import timezone

    try:
        car = Car.objects.get(plate_number=plate.upper()) 

        tickets = Ticket.objects.filter(car=car).order_by('-start_time').first()
        if tickets:
            if tickets.Parking.zone.service_provider.name != service_provider:
                return {
                    "type": "error",
                    "error": "wrong service provider.",
                    "ticket service provider": tickets.Parking.zone.service_provider.name,
                    "requested service provider": service_provider,
                }
            ticket_data = {
                "start_time": max(0, int(tickets.start_time.timestamp())) if tickets.start_time else 0,
                "stop_time": max(0, int(tickets.stop_time.timestamp())) if tickets.stop_time else 0,
            }
        else:
            ticket_data = {
                "start_time": 0,
                "stop_time": 0,
            }

        fines = Fine.objects.filter(car=car).order_by('-issued_time')[:3]
        last_fines = [
            int(f.issued_time.timestamp()) for f in fines if f.issued_time
        ]

        chalks = Chalk.objects.filter(car=car).order_by('-issued_time')[:3]
        last_chalks = [
            int(c.issued_time.timestamp()) for c in chalks if c.issued_time
        ]

        return {
            "type": "control_plate",
            "plate": car.plate_number,
            "ticket": ticket_data,
            "last_fines": last_fines,
            "last_chalks": last_chalks,
        }

    except Car.DoesNotExist:
        return {
            "type": "control_plate",
            "plate": plate,
            "ticket": {
                "start_time": 0,
                "stop_time": 0,
            },
            "last_fines": [],
            "last_chalks": [],
        }    
        
        
        
    except Exception as e:
        return {"type": "error", "error": f"Server error: {str(e)}"}

    #--------------------------------------------------------------------------------------------------
    
# TODO: create a function to emit a fine -> returns get_all_info_car(plate , service_provider)
# @database_sync_to_async
# def emit_fine(plate, service_provider):


# TODO: create a function to emit a chalk -> returns get_all_info_car(plate , service_provider)
# @database_sync_to_async
# def emit_chalk(plate, service_provider):
