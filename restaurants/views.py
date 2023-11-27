# views.py
from rest_framework import generics
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.permissions import IsAuthenticated
from .models import Feedback, Restaurant, Event, OpeningHours
from .serializers import RestaurantSerializer, EventSerializer, OpeningHoursSerializer, FeedbackSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from menus.models import Menu
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet


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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Restaurant.objects.filter(user_restaurant=self.request.user)

    def get_serializer_class(self):
        return RestaurantSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class EventCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        # Associate the event with the currently authenticated user's restaurant
        serializer.save(restaurant=self.request.user.restaurant)


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        # Get events for the currently authenticated user's restaurant
        return Event.objects.filter(restaurant=self.request.user.restaurant)


class OpeningHoursCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = OpeningHoursSerializer

    def perform_create(self, serializer):
        # Check if opening hours already exist for the restaurant
        opening_hours_instance = get_object_or_404(
            OpeningHours, restaurant=self.request.user.restaurant)

        # If opening hours exist, update them; otherwise, create new ones
        if opening_hours_instance:
            serializer.update(opening_hours_instance,
                              serializer.validated_data)
        else:
            serializer.save(restaurant=self.request.user.restaurant)


class OpeningHoursRetrieveView(generics.RetrieveAPIView):
    serializer_class = OpeningHoursSerializer

    def get_object(self):
        # Retrieve opening hours for the current user's restaurant
        opening_hours_instance = OpeningHours.objects.filter(
            restaurant=self.request.user.restaurant).first()

        if not opening_hours_instance:
            # You can customize the response if opening hours do not exist
            return Response({"detail": "Opening hours not found for this restaurant."},
                            status=404)

        return opening_hours_instance


class FeedbackCreateView(CreateAPIView):
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        restaurant_id = self.request.data.get('restaurant')
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        serializer.save(restaurant=restaurant)


class FeedbackListView(ListAPIView):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        restaurant_id = self.request.data.get('restaurant')
        return Feedback.objects.filter(restaurant_id=restaurant_id)


class FeedbackRetrieveView(RetrieveModelMixin, GenericViewSet):
    serializer_class = FeedbackSerializer

    def get_object(self):
        restaurant_id = self.request.data.get('restaurant')
        feedback_instance = Feedback.objects.filter(
            restaurant_id=restaurant_id).first()

        if not feedback_instance:
            # You can customize the response if feedbacks do not exist
            return Response({"detail": "Feedbacks not found for this restaurant."},
                            status=404)

        return feedback_instance
