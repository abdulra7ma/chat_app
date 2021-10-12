from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatRoomConsumer.as_asgi()),
    re_path(r"ws/messenger/(?P<username>\w+)/$", consumers.MessengerConsumer.as_asgi()),
    re_path(r"ws/$", consumers.SearchConsumer.as_asgi()),
]
