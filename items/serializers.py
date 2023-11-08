from rest_framework import serializers
from .models import Item
from media.serializers import MediaSerializer


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'
