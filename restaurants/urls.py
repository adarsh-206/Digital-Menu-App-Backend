# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/register', views.RestaurantListCreateView.as_view(),
         name='restaurant-list-create'),
    path('restaurants/detail/<int:pk>', views.RestaurantDetailView.as_view(),
         name='restaurant-detail'),
    path('restaurants/generate-qr-code',
         views.GenerateQRCode.as_view(), name='generate-qr-code'),
    path('restaurants/create/', views.EventCreateView.as_view(), name='event-create'),
    path('restaurants/events/', views.EventListView.as_view(), name='event-list'),
    path('restaurants/opening-hours/create/',
         views.OpeningHoursCreateView.as_view(), name='opening-hours-create'),
    path('restaurants/opening-hours/',
         views.OpeningHoursRetrieveView.as_view(), name='opening-hours-detail'),
    path('restaurants/feedbacks/',
         views.FeedbackCreateView.as_view(), name='create-feedback'),
    path('restaurants/feedbacks/list/',
         views.FeedbackListView.as_view(), name='list-feedbacks'),
    path('restaurants/feedbacks/detail/', views.FeedbackRetrieveView.as_view(
        {'get': 'retrieve'}), name='retrieve-feedback'),
]
