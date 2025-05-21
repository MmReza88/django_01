import json
from channels.generic.websocket import AsyncWebsocketConsumer

#-------------------------------------------------------------------------------------


class MessageConsumer(AsyncWebsocketConsumer):
    

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if self.client_id:
            await self.channel_layer.group_discard(self.client_id, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Decoded control_admin data : {data}")

    
    
    async def send_login(self, event):
        print("Send a login")
        await self.send(text_data=json.dumps({
            "type": "login",
            "username": event["username"],
        }))
        self.client_username = event["username"]
    
    async def send_start(self, event):
        print("sending start because card is here")
        await self.send(text_data=json.dumps({
            "type": "start",
        }))
