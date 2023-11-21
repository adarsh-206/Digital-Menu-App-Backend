# menus/models.py
from django.db import models
from restaurants.models import Restaurant
from categories.models import Category
from items.models import Item


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    menu_description = models.TextField(blank=True, null=True)
    launch_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.menu.name} - {self.item.name}"
