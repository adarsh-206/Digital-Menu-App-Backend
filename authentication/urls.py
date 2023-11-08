from django.urls import path, include
from . import views

urlpatterns = [
    path('user/register', views.UserRegistrationView.as_view(),
         name='user-register'),
    path('user/login', views.UserLoginView.as_view(), name='user-login'),
    path('user/details', views.UserDetailsView.as_view(), name='user-details'),
    path('user/logout', views.LogoutView.as_view(), name='logout'),
    path('user/has-restaurant', views.UserHasRestaurantView.as_view(),
         name='user-has-restaurant'),
]
