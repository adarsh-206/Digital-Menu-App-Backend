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
        has_restaurants = Restaurant.objects.filter(user=user).exists()
        # Return the result as a JSON response
        return Response({'registered': has_restaurants}, status=status.HTTP_200_OK)
