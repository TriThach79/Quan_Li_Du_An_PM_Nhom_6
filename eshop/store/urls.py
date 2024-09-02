from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .forms import UserLoginForm
# from .forms import ResetPasswordForm, ResetConfirmForm


app_name = 'store'
urlpatterns = [
    path('', views.product_all, name = 'product_all'),
    path('item/<slug:slug>/', views.product_detail, name = 'product_detail'),
    path('search/<slug:category_slug>/', views.category_list, name='category_list'),
    path('account/register/', views.user_register, name='register'),
    path('account/<slug:uidb64>/<slug:token>/', views.user_activate, name='activate'),
    path('account/login/', auth_views.LoginView.as_view(template_name='account/login.html',
    form_class = UserLoginForm), name = 'login'),
    path('account/logout/', auth_views.LogoutView.as_view(next_page='store:login'),
    name = 'logout'),

]