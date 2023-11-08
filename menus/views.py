from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Menu, MenuItem
from .serializers import MenuSerializer, MenuItemSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from items.models import Item
from categories.models import Category


class MenuListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuAddItemView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = MenuItemSerializer

    def create(self, request, menu_id):
        try:
            menu = Menu.objects.get(id=menu_id)
        except Menu.DoesNotExist:
            return Response({"error": "Menu does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Get the category and parent category from the request data
        category_id = request.data.get("category")
        parent_category_id = request.data.get("parent_category")

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            parent_category = Category.objects.get(id=parent_category_id)
        except Category.DoesNotExist:
            return Response({"error": "Parent category does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Create a new menu item
        menu_item_data = {
            "menu": menu.id,
            "item": category.item_set.first().id,
            "quantity": 1,
            "category": category_id,
            "parent_category": parent_category_id,
        }

        serializer = self.get_serializer(data=menu_item_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
