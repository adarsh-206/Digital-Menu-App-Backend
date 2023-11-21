# items/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
    path('items/category/<int:category_id>/subcategory/<int:subcategory_id>/',
         ItemViewSet.as_view({'get': 'list'}), name='item-list-by-category-subcategory'),
]
