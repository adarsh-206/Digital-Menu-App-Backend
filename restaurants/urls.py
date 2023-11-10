# restaurant/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet

# Create a router and register the RestaurantViewSet with it.
router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
