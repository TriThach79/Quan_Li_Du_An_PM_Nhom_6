
from django.shortcuts import get_object_or_404,render
from django.urls import reverse
import uuid
from cart.cart import Cart
from store.models import Order, OrderItem, Stock, Product
from django.db.models import F
from django.conf import settings
from decimal import Decimal
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from store.forms import CheckoutForm
from paypal.standard.forms import PayPalPaymentsForm
import pytz

tz_vn = pytz.timezone('Asia/Ho_Chi_Minh')

@login_required
def paypal_form(request):
    # order_id = request.session.get('order_id')
    # order = get_object_or_404(Order, id=order_id)
    cart = Cart(request)
    order_key = uuid.uuid4()
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        # 'amount': '%.2f' % order.total_cost().quantize(
        #     Decimal('.01')),
        'amount': '30.00',
        # 'item_name': 'Order {}'.format(order.id),
        'item_name': f'Order_{datetime.now().astimezone(tz=tz_vn).strftime("%Y%m%d-%H%M%S")}',
        # 'invoice': str(order.id),
        'invoice': order_key,
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('checkout:payment-successful')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('checkout:payment-failed')),
    }



    form = PayPalPaymentsForm(initial=paypal_dict)
    if request.method == 'POST':
        info_form = CheckoutForm(request.POST)
        if info_form.is_valid():
            order = info_form.save(commit=False)
            order.user = request.user
            order.full_name = request.POST['full_name']
            order.phone = request.POST['phone_number']
            order.address1 = request.POST['address_1']
            order.total_paid = 0
            order.order_key = uuid.uuid4()
            order.billing_status = False
            order.save()

            # full_name = request.POST['full_name']
            # print(type(full_name))

    else:
        info_form = CheckoutForm()
    return render(request, 'checkout/paypal_integration.html', {'form': form, 'info_form': info_form})

@csrf_exempt
def payment_completed(request):
    cart = Cart(request)
    order_key = uuid.uuid4()
    user_id = request.user
    order = Order.objects.filter(user = user_id).first()
    # print(order)
    # full_name = request.POST['full_name']
    # phone = request.POST['phone_number']
    # address = request.POST['address_1']

    # if Order.objects.filter(order_key = order_key).exists():
    #     pass
    # else:
    #     order = Order.objects.create(user_id = user_id, full_name = 'full_name', address1 = 'address', phone = '0853789410',
    #                                         address2 = 'add2', total_paid = cart.total_cart_price(), order_key = order_key)
    #     for item in cart:
    #         OrderItem.objects.create(order = order , product = item['product'], price = item['price'], quantity = item['soluong'])   
    for item in cart:
        OrderItem.objects.create(order = order , product = item['product'], price = item['price'], quantity = item['soluong'])   
        s = Stock.objects.filter(product=item['product'])
        s.update(stock_quantity = F('stock_quantity') - item['soluong'])
        if s.first().stock_quantity <= 0:
            Product.objects.filter(id = item['product'].id).update(is_active = False)
            
    # Order.objects.filter(order_key= order.order_key).update(billing_status=True)
    Order.objects.filter(id = order.id).update(billing_status=True, total_paid = cart.total_cart_price())

    cart.clear()
    return render(request, 'checkout/payment_successful.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'checkout/payment_failed.html')

