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
