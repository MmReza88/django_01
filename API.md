# API Documentation

## TOTEM flutter app 
### request :
    http://127.0.0.1:8000/totem/totem_123/
### get_totem_infos(totem_id)
totem_id : String under the form `totem_XXX` where XXX is the id in the database of the totem.

Return exemple JSON object:
```json
{
    "parking_name": "Parco Pipo",
    "durations": [0, 10, 60, 120],
    "prices": [0, 0, 10, 50]
}
```

### get_user_cars(username)
username: unique username of a user in the Users table.

Returns a list with the plates of the user:

Exemple JSON object:
```json
{
    "plates": ["XXAA55", "ABCSED", "HAHAHA"]
}
```

### new_ticket(duration, totem_id, plate)
duration : int in minutes of the duration of the ticket
totem_id : String under the form `totem_XXX` where XXX is the id in the database of the totem.
plate: Str of the plate of a car

Creates a new entry in the `Ticket` table which is not payed yet.

Return JSON objectabout the status:
```json
{
    "status": "success"
}
```
"success" or "failed" are the two only values possible.

### get_car_parking_status(plate)
plate: Str of the plate of a car

Return JSON object: 
```json
{
    "time_left": 10
}
```
The time left is positive or 0 if the parking is not valid. and is the amount of minutes left. You will most likely have to look in the Tickets table to find the last one.

### pay_ticket(ticket_id)
ticket_id: id of the ticket which is paid for.

Mark the ticket as paid.

Return JSON objectabout the status:
```json
{
    "status": "success"
}
```
"success" or "failed" are the two only values possible.
