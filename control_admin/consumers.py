import json
from park_auth import api_functions
from channels.generic.websocket import AsyncWebsocketConsumer

#-------------------------------------------------------------------------------------


class MessageConsumer(AsyncWebsocketConsumer):
    client_id = None
    username = None
    service_provider = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if self.client_id:
            await self.channel_layer.group_discard(self.client_id, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Decoded control_admin data : {data}")
        if data["type"] == "startup":
            self.client_id = data["client_id"]
            await self.channel_layer.group_add(self.client_id, self.channel_name)
        elif data["type"] == "control_plate":
            response_data = await api_functions.get_all_info_car(data["plate"], self.service_provider)
            await self.send(text_data=json.dumps(response_data))
    
    async def send(self, text_data):
        print("Sending data:", text_data)  # Print what you're sending
        await super().send(text_data=text_data)      # Call the original send (optional)
    
    async def send_login(self, event):
        print("Send a login")
        await self.send(text_data=json.dumps({
            "type": "login",
            "username": event["username"],
            "group": "controller",
        }))
        self.client_username = event["username"]
        self.service_provider = event["service_provider"]
        
