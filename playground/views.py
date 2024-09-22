from django.http import HttpResponse
from django.shortcuts import render

from store.models import Order, OrderItem, Product


def say_hello(request):
    products = Product.objects.filter(unit_price__range=(20,30))
    # ordered = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')
    Order.objects.select_related('customer').prefetch_related('orderitem_set').order_by('-placed-at')[:5]
    ordered = Product.objects.filter(OrderItem.objects.select_related('order__customer')[:5]).order_by('title')
    return render(request, 'hello.html', {'name': 'Mosh', "products":products})
