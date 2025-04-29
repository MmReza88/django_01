from django.urls import re_path
from park_auth import consumers
# from pages import consumers

websocket_urlpatterns = [
    re_path(r"ws/login/$", consumers.MessageConsumer.as_asgi()),
]