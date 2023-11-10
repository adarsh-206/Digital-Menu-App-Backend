# items/models.py
from django.db import models
from categories.models import Category


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_veg = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ratings = models.DecimalField(max_digits=3, decimal_places=2)
    ingredients = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    subcategory = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name
