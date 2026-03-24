from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
    r'ws/session/admin/(?P<session_id>[0-9a-fA-F-]{36})/$',
    consumers.AdminConsumer.as_asgi()
    ),
    re_path(
    r'ws/session/client/',
    consumers.ClientConsumer.as_asgi()
    ),
]