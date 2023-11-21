# menu/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, MenuItemViewSet, MenuUpdateView, MenuDeleteView, CheckMenuItemAdded, RemoveMenuItemView, SortedItemsView, SetLaunchStatusFalse, FilteredItemsView

router = DefaultRouter()
router.register(r'menus', MenuViewSet, basename='item')
router.register(r'menu-items', MenuItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
    path('menus/<int:pk>/update/', MenuUpdateView.as_view(), name='menu-update'),
    path('menus/<int:pk>/delete/', MenuDeleteView.as_view(), name='menu-delete'),
    path('check-menu-item-added/<int:item_id>/<int:menu_id>/',
         CheckMenuItemAdded.as_view(), name='check-menu-item-added'),
    path('menus/<int:menu_id>/remove-item/<int:item_id>/',
         RemoveMenuItemView.as_view(), name='remove-menu-item'),
    path('sorted-items/', SortedItemsView.as_view(), name='sorted-items'),
    path('menus/set_launch_status_false/<int:menu_id>/',
         SetLaunchStatusFalse.as_view(), name='set_launch_status_false'),
    path('filtered-items/', FilteredItemsView.as_view(), name='filtered_items'),
]
