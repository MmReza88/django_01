import json
from channels.generic.websocket import AsyncWebsocketConsumer

#-------------------------------------------------------------------------------------


class MessageConsumer(AsyncWebsocketConsumer):
    client_id = None
    username = None
    group = None

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
            response_data = {
                "type": "control_plate",
                "username": "some",
                "ticket_info": {
                    "start": 0,
                    "end": 1748006179,
                },
                "last_fines": [1748006179],
                "last_chalks": [1748006000]
            }
            await self.send(text_data=json.dumps(response_data))
    
    
    async def send_login(self, event):
        print("Send a login")
        await self.send(text_data=json.dumps({
            "type": "login",
            "username": event["username"],
            "group": "controler"
        }))
        self.client_username = event["username"]
