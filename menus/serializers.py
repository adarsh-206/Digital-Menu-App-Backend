# menus/serializers.py
from rest_framework import serializers
from .models import Menu, MenuItem
from categories.models import Category
from categories.serializers import CategorySerializer
from items.models import Item
from items.serializers import ItemSerializer


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = '__all__'
