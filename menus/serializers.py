# menus/serializers.py
from rest_framework import serializers
from .models import Menu, MenuItem
from categories.models import Category
from categories.serializers import CategorySerializer
from items.models import Item
from items.serializers import ItemSerializer


class MenuItemSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = MenuItem
        fields = '__all__'

    def validate(self, data):
        menu = data['menu']
        item = data['item']

        if MenuItem.objects.filter(menu=menu, item=item).exists():
            raise serializers.ValidationError(
                "This item is already in the menu.")

        return data


class MenuSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(
        source='menuitem_set', many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'
