from django.urls import  path
from chat.consumer import ChatConsumer
from tweets.consumer import TwitterConsumer


websocket_urlpatterns = [
    path("ws/chat/<str:username>/", ChatConsumer.as_asgi()),
    path("ws/home/", TwitterConsumer.as_asgi()),
]



