# menu/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, MenuItemViewSet, MenuUpdateView, MenuDeleteView

router = DefaultRouter()
router.register(r'menus', MenuViewSet)
router.register(r'menu-items', MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('menus/<int:pk>/update/', MenuUpdateView.as_view(), name='menu-update'),
    path('menus/<int:pk>/delete/', MenuDeleteView.as_view(), name='menu-delete'),
]
