from rest_framework import serializers
from beermanagment.models import Reference, Bar, Stock, Order, OrderItem
from django.contrib.auth.models import User, Group


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reference
        fields = ['id', 'reference', 'name', 'description', 'availability', 'url']


class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
        fields = ['id', 'name', 'url']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['reference', 'bar', 'stock']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['reference', 'count']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'bar', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for i in items_data: OrderItem.objects.create(order=order, **i)
        return order

    

