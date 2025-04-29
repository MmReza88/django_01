import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


@database_sync_to_async
def get_totem_infos(totem_id):
    from pages.models import Totem  # Direct model import for clarity
    
    try:
        numeric_id = totem_id.split('_')[1]
        totem = Totem.objects.select_related("parking__zone").get(identity_code=numeric_id)

        # Convert prices and durations to lists
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


class MessageConsumer(AsyncWebsocketConsumer):
    client_id = None
    client_username = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if self.client_id:
            await self.channel_layer.group_discard(self.client_id, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "set_client_id":
            self.client_id = data["client_id"]
            await self.channel_layer.group_add(self.client_id, self.channel_name)

        elif data["type"] == "get_totem_infos":
            totem_id = data["totem_id"]
            response_data = await get_totem_infos(totem_id)
            await self.send(text_data=json.dumps(response_data))

    async def send_login(self, event):
        await self.send(text_data=json.dumps({
            "type": "login",
            "username": event["username"]
        }))
        self.client_username = event["username"]
