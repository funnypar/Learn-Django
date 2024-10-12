from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Collection, OrderItem, Product
from .serializers import CollectionSerializer, ProductSerializer


# Products
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter( product_id = kwargs['id']).count() > 0 :
            return Response({'error': 'Product can not be deleted ! Because that has "orderItem"'},status= status.HTTP_501_NOT_IMPLEMENTED)
        
        return super().destroy(request, *args, **kwargs)
    
    
# Collections
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter( product_id = kwargs['id']).count() > 0 :
            return Response({'error': 'Collection can not be deleted ! Because that has "products"'},status= status.HTTP_501_NOT_IMPLEMENTED)
        
        return super().destroy(request, *args, **kwargs)
        
    

    