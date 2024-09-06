from urllib import response
from django.shortcuts import get_object_or_404, render
from .cart import Cart
from django.contrib import messages
from django.http import JsonResponse
from store.models import Product
# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    print(cart.__len__())
    if (cart.__len__() == 0):
        messages.error(request, "Không có sản phẩm nào trong giỏ để đặt")
    return render(request, 'cart/summary.html', {'cart': cart})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id = product_id)
        cart.add(product=product, qty = product_qty)

        cart_qty = cart.__len__()
        response = JsonResponse({'soluong': cart_qty})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))

        cart.delete(product = product_id)

        cart_qty = cart.__len__()
        cart_total = cart.total_cart_price()
        response = JsonResponse({'cartqty': cart_qty, 'totalcartprice': cart_total})
        # return render(request, 'cart/summary.html', response)
    return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))

        cart.update(product = product_id, product_qty = product_qty)

        cart_qty = cart.__len__()
        cart_total = cart.total_cart_price()
        item_total = cart.total_item_price(str(product_id))
        response = JsonResponse({'cartqty': cart_qty, 'totalcartprice': cart_total, 'itemtotal': item_total})
        # return render(request, 'cart/summary.html', response) 
        return response

