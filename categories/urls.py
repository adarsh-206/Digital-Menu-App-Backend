# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/<int:pk>/subcategories/',
         CategoryViewSet.as_view({'get': 'subcategories'}), name='category-subcategories'),
    path('categories/top/',
         CategoryViewSet.as_view({'get': 'top_categories'}), name='top-categories'),
]
