# menu/views.py
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, RetrieveDestroyAPIView
from .models import Menu, MenuItem
from .serializers import MenuSerializer, MenuItemSerializer
from rest_framework.response import Response
from rest_framework import status


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def update_menu_name(self, request, pk=None):
        try:
            menu = Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)

        new_name = request.data.get('name')
        if new_name:
            menu.name = new_name
            menu.save()
            return Response(MenuSerializer(menu).data)
        else:
            return Response({'error': 'New menu name is required'}, status=status.HTTP_400_BAD_REQUEST)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuUpdateView(UpdateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuDeleteView(RetrieveDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
