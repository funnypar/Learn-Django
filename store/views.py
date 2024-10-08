from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer


# Products
class ProductList(APIView):
    def get(self, request):
        products = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = ProductSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get(self, request,id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    def put(self, request,id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    def delete(self, request,id):
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
# Collections
class CollectionList(APIView):
    def get(self, request):
        collections = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CollectionSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class CollectionDetail(APIView):
    def get(self, request,pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    def put(self, request,pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        serializer = CollectionSerializer(collection, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    def delete(self, request,pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        if collection.prodcuts.count() > 0 :
            return Response({'error': 'Collection can not be deleted ! Because that has "products"'},status= status.HTTP_501_NOT_IMPLEMENTED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        