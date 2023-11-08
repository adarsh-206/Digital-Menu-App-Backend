from rest_framework import serializers
from .models import Restaurant
from authentication.models import User


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = '__all__'
