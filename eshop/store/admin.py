from django.contrib import admin
from django.urls.resolvers import URLResolver
from .models import Category, Product, User, Order, OrderItem, Stock
from django.urls import path
from datetime import datetime
from django.template.response import TemplateResponse

# Register your models here.
class CustomAdminSite(admin.AdminSite):
    site_header = 'Web bán hàng mỹ phẩm'
    site_title = 'Hasake Admin Page'

custom_admin_site = CustomAdminSite('Hasake Admin Page')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','created','user_id','total_paid','billing_status')
    list_editable = ('billing_status',)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','order','product','price', 'quantity')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'category', 'price', 'in_stock', 'is_active')
    list_editable = ('is_active',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'is_superuser', 'first_name', 'last_name', 'email')

class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'stock_quantity', 'from_date', 'to_date')

custom_admin_site.register(Category)
custom_admin_site.register(Product, ProductAdmin)
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Order, OrderAdmin)
custom_admin_site.register(OrderItem, OrderItemAdmin)
custom_admin_site.register(Stock, StockAdmin)

