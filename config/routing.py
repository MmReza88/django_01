from django.urls import re_path
from park_auth import consumers as auth_consumers
from control_admin import consumers as control_consumers


websocket_urlpatterns = [
    re_path(r"ws/login/$", auth_consumers.MessageConsumer.as_asgi()),
    re_path(r"ws/control/$", control_consumers.MessageConsumer.as_asgi())
]