# categories/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from .models import Category
from .serializers import CategorySerializer
from menus.models import MenuItem
from rest_framework import status


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Filter categories based on the logged-in user's associated restaurant
        user = self.request.user
        if user.is_authenticated and user.restaurant:
            # If the user is associated with a restaurant, filter categories based on that restaurant
            return Category.objects.filter(restaurant=user.restaurant, parent_category__isnull=True)
        else:
            # If the user is not associated with a restaurant, return an empty queryset
            return Category.objects.none()

    def subcategories(self, request, pk=None):
        category = self.get_object()
        subcategories = category.subcategories.all()
        serializer = CategorySerializer(
            subcategories, many=True, context={'request': request})
        return Response(serializer.data)
