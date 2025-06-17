import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . import api_functions

#-------------------------------------------------------------------------------------


class MessageConsumer(AsyncWebsocketConsumer):
    client_id = None
    client_username = None
    card = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if self.client_id:
            await self.channel_layer.group_discard(self.client_id, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Decoded totem data : {data}")
    
        if data["type"] == "set_client_id":
            self.client_id = data["client_id"]
            await self.channel_layer.group_add(self.client_id, self.channel_name)
        elif data["type"] == "get_all_parkings":
            response_data = await api_functions.get_all_parkings()
            await self.send(text_data=json.dumps(response_data))
        elif data["type"] == "get_parking_infos":
            parking_name = data["parking_name"]
            response_data = await api_functions.get_parking_infos(parking_name)
            await self.send(text_data=json.dumps(response_data))
        elif data["type"] == "start_card":
            self.card = data["card"]
        elif data["type"] == "get_totem_infos":
            totem_id = data["totem_id"]
            response_data = await api_functions.get_totem_infos(totem_id)
            await self.send(text_data=json.dumps(response_data))
        elif data["type"] == "get_user_cars":
            username = data["username"]
            response_data = await api_functions.get_user_cars(username)
            await self.send(text_data=json.dumps(response_data))
        elif data["type"] == "create_new_ticket":
            duration = data["duration"]
            price = data["price"]
            totem_id = data["totem_id"]
            plate = data["plate"]
            token = data["token"]
            response_data = await api_functions.new_ticket(duration, price, totem_id, token, plate, self.card)
            await self.send(text_data=json.dumps(response_data))
        elif data["type"] == "get_car_parcking_status":
            plate = data["plate"]
            response_data = await api_functions.get_car_parking_status(plate)
            await self.send(text_data=json.dumps(response_data))


        else:
            response_data = {
                "type": "error",
                "error": "Invalid request type."
            }
            await self.send(text_data=json.dumps(response_data))
    
    
    async def send_login(self, event):
        print("Send a login")
        await self.send(text_data=json.dumps({
            "type": "login",
            "username": event["username"],
        }))
        self.client_username = event["username"]
    
    async def send_start(self, event):
        print("sending start because card is here")
        self.card = event["card"]
        await self.send(text_data=json.dumps({
            "type": "start",
        }))
    
    async def send(self, text_data):
        print("Sending data:", text_data)  # Print what you're sending
        await super().send(text_data=text_data)      # Call the original send (optional)

