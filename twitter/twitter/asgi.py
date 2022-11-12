
import os


from django.core.asgi import get_asgi_application
import django
from twitter.channelsmiddleware import JwtAuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from . import routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitter.settings')
django.setup()

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http" :  get_asgi_application(),
     "websocket": JwtAuthMiddlewareStack(
       URLRouter(
           routing.websocket_urlpatterns
        )
   )
})







