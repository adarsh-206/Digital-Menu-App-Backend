# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/register', views.RestaurantListCreateView.as_view(),
         name='restaurant-list-create'),
    path('restaurants/detail/<int:pk>', views.RestaurantDetailView.as_view(),
         name='restaurant-detail'),
]
