# menu/models.py
from django.db import models
from restaurants.models import Restaurant
from items.models import Item
from categories.models import Category


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    parent_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='parent_items')

    def __str__(self):
        return f"{self.item.name} in {self.menu.name}"
