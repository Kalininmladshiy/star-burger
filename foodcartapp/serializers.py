from rest_framework import serializers
from .models import Order
from phonenumber_field.serializerfields import PhoneNumberField


class GetOrderSerializer(serializers.ModelSerializer):
    phonenumber = PhoneNumberField()
    id = serializers.IntegerField()
    class Meta:
        model = Order
        fields = ('id', 'firstname', 'lastname', 'phonenumber', 'address')
