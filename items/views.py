# items/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from .models import Item
from .serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        category = serializer.validated_data['category']
        subcategory = serializer.validated_data.get('subcategory')
        if subcategory:
            serializer.save()
        else:
            serializer.save(subcategory=category)
