import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

import django
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from cart.routing import websocket_urlpatterns

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": ASGIStaticFilesHandler(django_asgi_app),  
    "websocket": URLRouter(websocket_urlpatterns),
})