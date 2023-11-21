# items/serializers.py
from rest_framework import serializers
from .models import Item
from rest_framework import generics


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
