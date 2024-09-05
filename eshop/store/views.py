from collections import Counter
import imp
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, DateField
from datetime import datetime
from .tokens import activation_token
from .models import User, Order, OrderItem
from django.http import HttpResponse
from django.db.models import Q
from django.db.models.functions import Cast
from functools import reduce
import operator
from django.db.models.functions import TruncMonth,ExtractMonth, ExtractYear

from django.core.mail import EmailMessage
from django.core.paginator import Paginator

from .models import Category, Product
from .forms import (CreateUserForm)
# Create your views here.


def product_all(request):
    products = Product.products.all()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    order_items = OrderItem.objects.values('product').annotate(sum_quantity = Sum('quantity')).order_by('-sum_quantity')

    # lọc product theo cách này thì được nhưng nó không còn theo thứ tự sum_quantity nữa
    #  mà nó tự sắp xếp theo thứ tự id product
    # p = products.filter(id__in=orderitem.values('product'))[:8]

    # Nên phải lấy từng id product trong top_8_product và query lại thông tin từng product rồi append vào list l
    best_selling_products = []
    for i in order_items.values('product'):
        id = i['product']
        prod = Product.objects.filter(id = id)
        best_selling_products.append(prod)

    return render(request, 'store/home.html', {'products': products, 'page_obj': page_obj, 'best_selling_products': best_selling_products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug = slug, in_stock = True)
    return render(request, 'products/detail.html', {'product': product})

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug = category_slug)
    products = Product.products.filter(category = category)

    return render(request, 'products/category.html', {'category': category, 'products': products})

def search(request):
    q=request.GET.get('q')
    sorting = request.GET.get('sorting')
    data=Product.objects.filter(Q(title__icontains = q) | Q(category__title__icontains = q)).order_by('-id')
    if sorting == 'asc':
        data = data.order_by('price')
    if sorting == 'desc':
        data = data.order_by('-price')
    if sorting == 'latest':
        data = data.order_by('created')
    if not data.count():
        messages.error(request,'Không tìm thấy sản phẩm!')
    return render(request,'products/search.html',{'data':data})

def user_register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        # We don't want anyone can be able to register account if they don't
        # actually post any data to us so this if will provide validation check.

        form = CreateUserForm(request.POST)
        # Create a form instance with POST data
        if form.is_valid():
            user = form.save(commit= False)
            # This save() method accepts an optional commit keyword argument, which accepts either True or False. 
            # If you call save() with commit=False, then it will return an object that hasn't yet been saved to the database.
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            # user.username = form.cleaned_data['user_name']
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            # Set is_active = False vì cần 1 thủ tục kích hoạt via email để is_active = True
            user.save()

            #Setup email
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/activate_account.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # encoding a byte string into base64 string so we can use it in the url,
                'token': activation_token.make_token(user),
            })
            # user.email_user(subject = subject, message = message)
            email = EmailMessage(subject = subject, body = message, to= [user.email])
            if email.send():
                # return HttpResponse("Registration Successful !" f'Dear <b>{user}</b>, please go to you email <b>{user.email}</b> inbox and click on \
                # received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.' )
                messages.success(request, 'Đã gửi mail kích hoạt tài khoản!'f' Hãy kiểm tra mail {user.email}')
            else:
                return HttpResponse(request, f'Problem sending email to {user.email}, check if you typed it correctly.')
    else:
        form = CreateUserForm()
    return render(request, 'account/register.html', {'form': form})


def user_activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    try:
        pass
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Kích hoạt tài khoản thành công! Giờ bạn có thể đăng nhập với tài khoản vừa tạo')
        return redirect('store:login')
    else:
        return render(request, 'account/fail_to_activate.html')