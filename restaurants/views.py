# views.py
from rest_framework import generics
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.permissions import IsAuthenticated
from .models import Restaurant
from .serializers import RestaurantSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User
import qrcode
from django.http import HttpResponse
from io import BytesIO
from django.conf import settings
from menus.models import Menu


class RestaurantListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(user_restaurant=self.request.user)

    def perform_create(self, serializer):
        # Create the restaurant
        restaurant = serializer.save()

        # Associate the restaurant with the currently authenticated user
        user = self.request.user
        user.restaurant = restaurant
        user.save()


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class CheckRestaurantRegistration(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        user = request.user

        # Check if the user has any associated restaurants
        restaurant = Restaurant.objects.filter(user=user).first()

        if restaurant:
            serializer = RestaurantSerializer(restaurant)
            return Response({'registered': True, 'restaurant_info': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'registered': False}, status=status.HTTP_200_OK)


class GenerateQRCode(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        # Get the current user's restaurant
        restaurant = request.user.restaurant

        # Get the menu ID from the query parameters
        menu_id = request.query_params.get('menu_id')

        if not menu_id:
            return Response({'error': 'Menu ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Set launch_status=True for the specified menu
        try:
            menu = restaurant.menu_set.get(id=menu_id)
        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)

        menu.launch_status = True
        menu.save()

        # Construct the menu URL with GST number and menu ID
        menu_url = f'{settings.FRONTEND_BASE_URL}/menu/{restaurant.gst_no}/{menu_id}'

        # Return the menu URL in the API response
        return Response({'qr_code_link': menu_url})
