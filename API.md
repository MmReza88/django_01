# API Documentation

## TOTEM flutter app 

### emit_new_chalk(plate) 

create a new chalk and create car in the db if it does not already exists

return:
```json
{"type": "success"}
```

### emit_new_fine(plate)

create a new fine and create car in the db if it does not already exists

return:
```json
{"type": "success"}
```

### get_user_for_badge(badge_number)

returns an error if the user is anything else than a controller

return:
```json
{
    "username": "biiopboopm",
    "group": "controller",
    "service_provider": "some_random_service_provider_name"
}
```

### get_all_info_car(plate_nb, service_provider)

if the service provider is not the good one:
```json
{"type": "error", "error": "wrong service provider"}
```

returns: 
```json
{
    "type": "control_plate",
    "parking_name": "some_random_parking_name",
    "ticket_info": {
        "start": 0, # timestamps
        "end": 0, # timestamps
    },
    "last_fines": [1748006179, 1748006179, 1748006179], # timestamps
    "last_chalks": [1748006000] # timestamps
}
```

### request :
    http://127.0.0.1:8000/api/totem/totem_xxx/
    e.g. : http://127.0.0.1:8000/api/totem/totem_321/
### get_totem_infos(totem_id)
totem_id : String under the form `totem_XXX` where XXX is the id in the database of the totem.

Return exemple JSON object:
```json        return {"type": "error", "error": "Invalid totem_id format."}

{
    "parking_name": "Parco Pipo",
    "durations": [0, 10, 60, 120],
    "prices": [0, 0, 10, 50]
}
```

### request :
    http://127.0.0.1:8000/api/user/cars/username/
    e.g. http://127.0.0.1:8000/api/user/cars/Eric/
### get_user_cars(username)
username: unique username of a user in the Users table.

Returns a list with the plates of the user:

Exemple JSON object:
```json
{
    "plates": ["XXAA55", "ABCSED", "HAHAHA"]
}
```

### new_ticket(duration , price , totem_id , plate) => written in pages/views
duration : int in minutes of the duration of the ticket
price : real in euro of the price of the ticket
totem_id : String under the form `totem_XXX` where XXX is the id in the database of the totem.
plate: Str of the plate of a car

Creates a new entry in the `Ticket` table which is not payed yet.

Return JSON objectabout the status:
```json
{
    "status": "success"
    "ticket id " : string
    "start time " : int (timestamp)
    "stop time " :  int (timestam)
}
```
"success" or "failed" are the two only values possible.

### get_car_parking_status(plate)  => written in pages/views
plate: Str of the plate of a car

Return JSON object: 
```json
{
    "time_left": 10
}
```
The time left is positive or 0 if the parking is not valid. and is the amount of minutes left. You will most likely have to look in the Tickets table to find the last one.

### pay_ticket(ticket_id)  => written in pages/views
ticket_id: id of the ticket which is paid for.

Mark the ticket as paid.

Return JSON objectabout the status:
```json
{
    "status": "success"
}
```
"success" or "failed" are the two only values possible.
