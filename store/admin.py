from typing import Any

from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models


# Register your models here.
class InventoryFilter(admin.SimpleListFilter):
    title='Inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<10','Low')
        ]
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10' :
            return queryset.filter(inventory__lt = 10)
        

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price','inventory_status','collection']
    list_per_page = 10
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update',InventoryFilter]
    prepopulated_fields = {'slug':['title']}
    autocomplete_fields = ['collection']
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory > 10 : 
            return "OK"
        return "LOW"
        
    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership","orders"]
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith','last_name__istartswith']

    @admin.display(ordering='products_count')
    def orders(self, customer):
        url = (reverse("admin:store_order_changelist") + "?" + urlencode({
            'customer__id':customer.id
        }))
        return format_html('<a href="{}">{}</a>', url , customer.orders_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(orders_count= Count('order'))
    
class OrderInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at','customer']
    autocomplete_fields = ['customer']
    inlines=[OrderInline]


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = (reverse("admin:store_product_changelist") + "?" + urlencode({
            'collection__id':str(collection.id)
        }))
        return format_html('<a href="{}">{}</a>', url , collection.products_count)
        
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(products_count= Count('product'))