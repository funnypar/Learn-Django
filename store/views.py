from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer


# Products
@api_view(['GET','PSOT'])
def product_list(request):
    if request.method == 'GET' :
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# Collections
@api_view()
def collection_list(request):
    collections = Collection.objects.annotate(products_count=Count('products')).all()
    serializer = CollectionSerializer(collections, many=True)
    return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if collection.prodcuts.count() > 0 :
            return Response({'error': 'Collection can not be deleted ! Because that has "products"'},status= status.HTTP_501_NOT_IMPLEMENTED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)