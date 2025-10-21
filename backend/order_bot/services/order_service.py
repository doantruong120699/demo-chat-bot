import json
import threading
from django.http import StreamingHttpResponse
from ..models import Order, OrderItem, Product, Category
from rest_framework import serializers
from queue import Queue

class StreamingOrderCallbackHandler:
    def __init__(self, queue: Queue):
        self.queue = queue
    def send(self, event_type: str, content=None):
        self.queue.put({"type": event_type, "content": content})

class OrderService:
    def __init__(self):
        self.queue = Queue()
        self.callback_handler = StreamingOrderCallbackHandler(self.queue)

    def list_orders(self):
        return Order.objects.all()

    def get_order(self, pk):
        return Order.objects.get(pk=pk)

    def create_order(self, data):
        items_data = data.pop('items', [])
        order = Order.objects.create(**data)
        total = 0
        for item in items_data:
            product = Product.objects.get(pk=item['product'])
            price = item.get('price', product.price)
            quantity = item.get('quantity', 1)
            OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
            total += price * quantity
        order.total_amount = total
        order.save()
        return order

    def stream_order_status(self, order_id):
        order = self.get_order(order_id)
        def run():
            self.callback_handler.send("start", {"status": order.status})
            # Simulate status update
            self.callback_handler.send("end", {"status": order.status})
        thread = threading.Thread(target=run)
        thread.start()
        while True:
            try:
                event = self.callback_handler.queue.get(timeout=1)
                yield f"data: {json.dumps(event)}\n\n"
                if event["type"] == "end":
                    break
            except:
                if not thread.is_alive():
                    break
