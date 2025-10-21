from rest_framework import serializers
from .models import Order, OrderItem, Product, Category

# Serializers
class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
	product = ProductSerializer(read_only=True)
	class Meta:
		model = OrderItem
		fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
	items = OrderItemSerializer(many=True, read_only=True)
	calc_total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
	class Meta:
		model = Order
		fields = '__all__'