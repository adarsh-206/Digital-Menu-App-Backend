# items/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from .models import Item
from .serializers import ItemSerializer
from rest_framework.response import Response
from rest_framework import status


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = ItemSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        subcategory_id = self.kwargs.get('subcategory_id')

        queryset = Item.objects.all()

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        if subcategory_id:
            queryset = queryset.filter(subcategory__id=subcategory_id)

        return queryset

    def perform_create(self, serializer):
        category = serializer.validated_data['category']
        subcategory = serializer.validated_data.get('subcategory')
        if subcategory:
            serializer.save()
        else:
            serializer.save(subcategory=category)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
