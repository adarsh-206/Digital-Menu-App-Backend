from .models import Category
from .serializers import CategorySerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    basename = 'category'

    def get_queryset(self):
       # Filter out only the top-level categories
        queryset = Category.objects.filter(parent_category__isnull=True)

        # Prefetch related items and subcategories for optimization
        return queryset.prefetch_related('items', 'subcategories')
