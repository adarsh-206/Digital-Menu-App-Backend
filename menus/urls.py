from django.urls import path
from menus.views import MenuListCreateView, MenuRetrieveUpdateDestroyView, MenuAddItemView

urlpatterns = [
    # List and create menus
    path('menus', MenuListCreateView.as_view(), name='menu-list-create'),

    # Retrieve, update, and delete a specific menu
    path('menus/<int:pk>', MenuRetrieveUpdateDestroyView.as_view(),
         name='menu-retrieve-update-destroy'),

    # Add items to a specific menu
    path('menus/<int:menu_id>/add-item/',
         MenuAddItemView.as_view(), name='menu-add-item'),
]
