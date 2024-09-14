from django.contrib import admin
from django.urls.resolvers import URLResolver
from .models import Category, Product, User, Order, OrderItem, Stock
from django.urls import path
from datetime import datetime
from django.template.response import TemplateResponse
from .views import number_order_by_month, revenue_by_month, number_order_by_day, revenue_by_day


# Register your models here.
class CustomAdminSite(admin.AdminSite):
    site_header = 'Web bán hàng mỹ phẩm'
    site_title = 'Hasake Admin Page'

    def get_urls(self) -> list[URLResolver]:
        return [
            path("chart/", self.stats_view, name='chart')
        ] + super().get_urls()
    
    def stats_view(self, request):
        month = request.GET.get('month', datetime.now().month)
        year = request.GET.get('year', datetime.now().year)
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        orders = Order.objects.filter(billing_status = True)
        # if Stock.objects.filter(product = 10).only('stock_quantity') == 3:
        #     print('yes')
        # else:
        #     print('no')
        r = Stock.objects.filter(product = 10).first()
        print(type(r))
        count_by_month = number_order_by_month(orders=orders,month=month, year=year, from_date=from_date, to_date=to_date)
        revenue_by_month_data = revenue_by_month(orders=orders ,month=month, year=year, from_date=from_date, to_date=to_date)
        count_by_day = number_order_by_day(orders=orders ,month=month, year=year, from_date=from_date, to_date=to_date)
        revenue_by_day_data = revenue_by_day(orders=orders ,month=month, year=year, from_date=from_date, to_date=to_date)
        # Order.objects.filter(id=61).update(created=datetime.strptime('07/09/2023', '%d/%m/%Y'))
        return TemplateResponse(request, "account/chart_stats.html", 
                                {'count_by_month': count_by_month, 'revenue_by_month': revenue_by_month_data, 
                                    'count_by_day': count_by_day, 'revenue_by_day': revenue_by_day_data})

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

