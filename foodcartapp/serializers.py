from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Product, Order, OrderItem
from phonenumber_field.serializerfields import PhoneNumberField

from django.db import transaction


class OrderItemSerializer(ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    price = serializers.IntegerField(required=False)

    class Meta:
        model = OrderItem
        fields = ['quantity', 'product', 'price']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False, source='order_items')
    phonenumber = PhoneNumberField()
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products', 'id']

    @transaction.atomic
    def create(self, validated_data):
        order_items_fields = validated_data.pop('order_items', None)
        new_order = Order.objects.create(**validated_data)
        order_items = [OrderItem(
            order=new_order,
            price=fields['product'].price,
            **fields,
        ) for fields in order_items_fields]
        OrderItem.objects.bulk_create(order_items)
        return new_order
