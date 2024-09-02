from distutils.command import upload
from enum import unique
from tabnanny import verbose
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime
from django.urls import reverse
from pkg_resources import require
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff = True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser = True')
        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_('Phải nhập email !'))
        
        email = self.normalize_email(email)
        user = self.model(email = email, username = username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique = True)
    avatar = models.ImageField(upload_to='user_images/')    
    phone_number = models.CharField(max_length = 11, blank = True)
    address_1 = models.CharField(max_length = 150, blank = True)
    address_2 = models.CharField(max_length = 150, blank = True)
    # username = models.CharField(max_length = 50, unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta: 
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.username

    

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)
        
class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, related_name = 'product', on_delete= models.CASCADE)
    created_by = models.ForeignKey(User, related_name = 'product_creator', on_delete = models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField(blank= True)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=9, decimal_places=0)
    old_price = models.DecimalField(max_digits=9, decimal_places=0)    
    objects = models.Manager()
    products = ProductManager()
    
    # class Meta:
    #     ordering = ('-created',)
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])
    
    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    full_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank = True, null = True)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places = 0)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
class Stock(models.Model):
    product = models.ForeignKey(Product, related_name='stock', on_delete=models.CASCADE)
    stock_quantity = models.IntegerField(default = 1)
    from_date = models.DateTimeField(auto_now_add=True)
    to_date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return str(self.id)
    


    
