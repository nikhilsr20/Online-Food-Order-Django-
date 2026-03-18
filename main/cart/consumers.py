from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.template.loader import render_to_string
import json
from partner.models import Order  

class RestaurantOrderCustomer(AsyncWebsocketConsumer):

    async def connect(self):
        self.restaurant_id = self.scope["url_route"]["kwargs"]["restaurant_id"]
        self.group_name = f"orders_{self.restaurant_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        print("✅ WS CONNECTED:", self.group_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def new_order(self, event):
        print("📩 EVENT RECEIVED:", event)   
        order_id = event["order_id"]

        order = await sync_to_async(Order.objects.prefetch_related("items").get)(id=order_id)

        html = await sync_to_async(render_to_string)(
            "partner/partner_orders_partial.html",
            {"order": order}
        )

        await self.send(text_data=html)
        print("📤 HTML SENT")    