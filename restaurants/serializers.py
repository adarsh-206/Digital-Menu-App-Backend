# restaurant/serializers.py
from rest_framework import serializers
from .models import Restaurant, Event, OpeningHours, Feedback


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        fields = '__all__'

    def to_internal_value(self, data):
        for day, value in data.items():
            # Extract 'open' or 'close' from the key
            time_type = day.split('_')[1]
            if value == "":
                data[day] = None

        return super().to_internal_value(data)


class RestaurantSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
