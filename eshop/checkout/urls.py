from django.urls import path
from . import views

app_name = 'checkout'
urlpatterns = [
    path('', views.paypal_form, name = 'paypal_checkout'),
    path('payment-successful/', views.payment_completed, name='payment-successful'),
    path('payment-failed/', views.payment_canceled, name='payment-failed'),
]