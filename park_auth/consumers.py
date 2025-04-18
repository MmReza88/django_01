from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MessageConsumer(AsyncWebsocketConsumer):
    client_id = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if self.client_id:
            await self.channel_layer.group_discard(self.client_id, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if "client_id" in data:            
            self.client_id = data["client_id"]
            # Add this socket to a group named with the ID
            await self.channel_layer.group_add(self.client_id, self.channel_name)

    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
    
    async def send_login(self, event):
        await self.send(text_data=json.dumps({
            "username": event["username"]
        }))
