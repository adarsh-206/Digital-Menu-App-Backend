# restaurant\model
from django.db import models


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    gst_no = models.CharField(max_length=15)
    fssai_code = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.restaurant_name


class Event(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()

    def __str__(self):
        return f"{self.restaurant.restaurant_name} - {self.event_name}"


class OpeningHours(models.Model):
    restaurant = models.OneToOneField(
        'Restaurant', on_delete=models.CASCADE, related_name='opening_hours', null=True, blank=True)
    monday_open = models.TimeField(null=True, blank=True)
    monday_close = models.TimeField(null=True, blank=True)
    tuesday_open = models.TimeField(null=True, blank=True)
    tuesday_close = models.TimeField(null=True, blank=True)
    wednesday_open = models.TimeField(null=True, blank=True)
    wednesday_close = models.TimeField(null=True, blank=True)
    thursday_open = models.TimeField(null=True, blank=True)
    thursday_close = models.TimeField(null=True, blank=True)
    friday_open = models.TimeField(null=True, blank=True)
    friday_close = models.TimeField(null=True, blank=True)
    saturday_open = models.TimeField(null=True, blank=True)
    saturday_close = models.TimeField(null=True, blank=True)
    sunday_open = models.TimeField(null=True, blank=True)
    sunday_close = models.TimeField(null=True, blank=True)


class Feedback(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    feedback_type = models.CharField(max_length=255)
    additional_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.restaurant.restaurant_name} - {self.user.username} Feedback"
