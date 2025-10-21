from django.core.management.base import BaseCommand
from order_bot.models import Category, Product, Order, OrderItem
import random

class Command(BaseCommand):
    help = 'Seed initial data for order_bot app'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding order_bot data...'))

        # Create categories
        categories = []
        for cat_name in ['Áo thun', 'Quần jeans', 'Áo khoác', 'Váy', 'Giày']:
            cat, _ = Category.objects.get_or_create(name=cat_name, defaults={"description": f"Danh mục {cat_name}"})
            categories.append(cat)

        # Create products
        products = []
        for i in range(1, 11):
            cat = random.choice(categories)
            prod, _ = Product.objects.get_or_create(
                name=f"Sản phẩm {i}",
                defaults={
                    "description": f"Mô tả sản phẩm {i}",
                    "price": random.randint(100, 500) * 1000,
                    "stock": random.randint(10, 100),
                    "image": f"https://picsum.photos/seed/{i}/200/200",
                    "category": cat,
                }
            )
            products.append(prod)

        # Create orders
        for i in range(1, 6):
            order = Order.objects.create(
                customer_name=f"Khách hàng {i}",
                customer_phone=f"09000000{i}",
                customer_address=f"Địa chỉ {i}",
                status=random.choice(["pending", "confirmed", "shipped", "done", "canceled"]),
            )
            total = 0
            for _ in range(random.randint(1, 3)):
                prod = random.choice(products)
                quantity = random.randint(1, 5)
                price = prod.price
                OrderItem.objects.create(order=order, product=prod, quantity=quantity, price=price)
                total += price * quantity
            order.total_amount = total
            order.save()

        self.stdout.write(self.style.SUCCESS('OrderBot seed data created successfully!'))
