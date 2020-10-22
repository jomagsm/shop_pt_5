from rest_framework import serializers

from webapp.models import Product, Order, OrderProduct
from django.contrib.auth import get_user_model

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderProduct
        fields = ('product', 'qty')

class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ('name', 'address', 'phone', 'order_products')

