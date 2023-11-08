from django.urls import path
from .views import ItemList, ItemDetail

urlpatterns = [
    path('items/list', ItemList.as_view(), name='item-list'),
    path('items/item-detail/<int:pk>', ItemDetail.as_view(), name='item-detail'),
]
