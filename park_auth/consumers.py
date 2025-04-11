from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("messages", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("messages", self.channel_name)

    async def receive(self, text_data):
        # Optional: receive from client
        pass

    async def send_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))