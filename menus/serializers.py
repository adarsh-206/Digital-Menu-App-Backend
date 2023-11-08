# menu/serializers.py
from rest_framework import serializers
from .models import Menu, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    # To display items as an array of item names
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Menu
        fields = '__all__'
