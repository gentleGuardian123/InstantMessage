# swt&&zwx
# time: 2023/6/22 10:42


from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_name>\w+)/(?P<user_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

