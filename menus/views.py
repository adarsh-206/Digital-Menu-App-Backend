# menu/views.py
from rest_framework.permissions import IsAuthenticated
from .serializers import MenuItemSerializer
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, RetrieveDestroyAPIView
from .models import Menu, MenuItem
from .serializers import MenuSerializer, MenuItemSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from io import BytesIO
from rest_framework import generics
import qrcode


class MenuViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = MenuSerializer

    def get_queryset(self):
        # Return only the menus associated with the logged-in user's restaurant
        return Menu.objects.filter(restaurant=self.request.user.restaurant)

    def perform_create(self, serializer):
        # Associate the new menu with the logged-in user's restaurant
        serializer.save(restaurant=self.request.user.restaurant)

    def update_menu_name(self, request, pk=None):
        try:
            menu = Menu.objects.get(pk=pk, restaurant=request.user.restaurant)
        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)

        new_name = request.data.get('name')
        if new_name:
            menu.name = new_name
            menu.save()
            return Response(MenuSerializer(menu).data)
        else:
            return Response({'error': 'New menu name is required'}, status=status.HTTP_400_BAD_REQUEST)


class MenuItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuDeleteView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class CheckMenuItemAdded(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request, item_id, menu_id):
        try:
            # Check if the menu item exists in the specified menu
            menu_item_exists = MenuItem.objects.filter(
                item_id=item_id, menu_id=menu_id).exists()

            return Response({'exists': menu_item_exists}, status=status.HTTP_200_OK)

        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item not found in the specified menu.'}, status=status.HTTP_404_NOT_FOUND)


class RemoveMenuItemView(DestroyAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def delete(self, request, menu_id, item_id):
        try:
            menu_item = MenuItem.objects.get(menu_id=menu_id, item_id=item_id)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item not found in the specified menu.'}, status=status.HTTP_404_NOT_FOUND)

        menu_item.delete()
        return Response({'success': 'Menu item removed successfully.'}, status=status.HTTP_200_OK)


class SortedItemsView(APIView):

    def get(self, request):
        try:
            gst_no = request.query_params.get('gst_no')
            menu_id = request.query_params.get('menu_id')
            is_veg = request.query_params.get('is_veg')
            is_non_veg = request.query_params.get('is_non_veg')
            min_price = request.query_params.get('min_price')
            max_price = request.query_params.get('max_price')

            # Ensure is_veg and is_non_veg are boolean values
            is_veg = is_veg.lower() == 'true' if is_veg else None
            is_non_veg = is_non_veg.lower() == 'true' if is_non_veg else None

            menus = Menu.objects.filter(id=menu_id, restaurant__gst_no=gst_no)

            sorted_items = []
            category_index = 0

            for menu in menus:
                menu_data = MenuSerializer(menu).data
                menu_items = MenuItem.objects.filter(menu=menu)

                categories = []

                for menu_item in menu_items:
                    item = menu_item.item
                    category_name = item.category.name
                    category_description = item.category.description
                    subcategory_name = item.subcategory.name if item.subcategory else None

                    # Filter based on is_veg and is_non_veg
                    if (
                        (is_veg is not None and item.is_veg == is_veg) or
                        (is_non_veg is not None and item.is_veg != is_non_veg)
                    ):
                        # Filter based on min_price and max_price
                        if (min_price is None or item.price >= float(min_price)) and \
                           (max_price is None or item.price <= float(max_price)):
                            item_data = {
                                "id": item.id,
                                "name": item.name,
                                "description": item.description,
                                "is_veg": item.is_veg,
                                "price": item.price,
                                "image": item.image.url if item.image else None,
                            }

                            # Check if the category already exists in categories list
                            category_exists = False
                            for category in categories:
                                if category["name"] == category_name:
                                    category_exists = True
                                    category_index = category["id"]
                                    break

                            if not category_exists:
                                # If category doesn't exist, create a new entry
                                category_index += 1
                                categories.append({
                                    "id": category_index,
                                    "name": category_name,
                                    "description": category_description,
                                    "subcategories": []
                                })

                            if subcategory_name:
                                # Check if subcategory already exists in the category's subcategories list
                                subcategory_exists = False
                                for subcategory in categories[category_index - 1]["subcategories"]:
                                    if subcategory["name"] == subcategory_name:
                                        subcategory_exists = True
                                        break

                                if not subcategory_exists:
                                    # If subcategory doesn't exist, create a new entry
                                    categories[category_index - 1]["subcategories"].append({
                                        "id": len(categories[category_index - 1]["subcategories"]) + 1,
                                        "name": subcategory_name,
                                        "items": []
                                    })

                                # Append item data to the subcategory
                                categories[category_index -
                                           1]["subcategories"][-1]["items"].append(item_data)
                            else:
                                # If item doesn't have a subcategory, append it directly to the category
                                categories[category_index -
                                           1]["items"].append(item_data)

                menu_data["categories"] = categories
                sorted_items.append(menu_data)

            return Response(sorted_items, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilteredItemsView(APIView):
    def get(self, request):
        try:
            gst_no = request.query_params.get('gst_no')
            menu_id = request.query_params.get('menu_id')
            search_query = request.query_params.get('q')

            menus = Menu.objects.filter(id=menu_id, restaurant__gst_no=gst_no)
            items_list = []

            for menu in menus:
                menu_data = MenuSerializer(menu).data
                menu_items = MenuItem.objects.filter(menu=menu)
                categories = []

                for menu_item in menu_items:
                    item = menu_item.item

                    # Check if the item matches the search query or filter criteria
                    if search_query and (
                        search_query.lower() in item.name.lower() or
                        search_query.lower() in item.description.lower()
                    ):
                        category_name = item.category.name
                        subcategory_name = item.subcategory.name if item.subcategory else None

                        # Check if the category exists
                        category_exists = any(
                            category["name"] == category_name for category in categories)

                        if not category_exists:
                            categories.append({
                                "id": len(categories) + 1,
                                "name": category_name,
                                "subcategories": [] if subcategory_name else None,
                                "items": [] if not subcategory_name else None
                            })

                        if subcategory_name:
                            subcategory_exists = any(
                                subcategory["name"] == subcategory_name
                                for subcategory in categories[-1]["subcategories"]
                            )

                            if not subcategory_exists:
                                categories[-1]["subcategories"].append({
                                    "id": len(categories[-1]["subcategories"]) + 1,
                                    "name": subcategory_name,
                                    "items": []
                                })

                            categories[-1]["subcategories"][-1]["items"].append({
                                "id": item.id,
                                "name": item.name,
                                "description": item.description,
                                "is_veg": item.is_veg,
                                "price": item.price,
                                "image": item.image.url if item.image else None,
                            })
                        else:
                            categories[-1]["items"].append({
                                "id": item.id,
                                "name": item.name,
                                "description": item.description,
                                "is_veg": item.is_veg,
                                "price": item.price,
                                "image": item.image.url if item.image else None,
                            })

                menu_data["categories"] = categories
                items_list.append(menu_data)

            return Response(items_list, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SetLaunchStatusFalse(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def post(self, request, menu_id):
        try:
            # Get the menu associated with the logged-in user's restaurant
            menu = Menu.objects.get(
                id=menu_id, restaurant=request.user.restaurant)

            # Set launch_status to False
            menu.launch_status = False
            menu.save()

            # Serialize the updated menu
            serialized_menu = MenuSerializer(menu).data

            return Response({'message': 'Launch status set to False', 'menu': serialized_menu}, status=status.HTTP_200_OK)

        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaveQRCodeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def post(self, request, gst_no, menu_id):
        try:
            # Get the current user's restaurant
            restaurant = request.user.restaurant

            # Get the menu associated with the restaurant and specified menu ID
            menu = Menu.objects.get(id=menu_id, restaurant=restaurant)

            # Generate QR code content (you may adjust this based on your requirements)
            qr_code_content = f'GST: {restaurant.gst_no}, Menu ID: {menu_id}'

            # Create a QR code using the qrcode library
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )
            qr.add_data(qr_code_content)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Save the QR code image to a BytesIO buffer
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_code_image = buffer.getvalue()

            # Update the menu with the QR code image
            menu.qr_code.save(f'qrcode_{menu.id}.png', BytesIO(qr_code_image))

            return Response({'message': 'QR code saved successfully'}, status=status.HTTP_200_OK)

        except Menu.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
