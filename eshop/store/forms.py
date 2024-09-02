from collections.abc import Mapping
import email
from typing import Any
from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import User, Order
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

class CreateUserForm(forms.ModelForm):
    username = forms.CharField(required= False,label = "Tài khoản",max_length=50, min_length=8, help_text= 'Required')
    email = forms.EmailField(max_length=100, help_text = "Required", error_messages={'required': 'Bạn phải nhập email'})
    password = forms.CharField(label = 'Mật khẩu', widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'Nhập lại mật khẩu', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['username'].lower()
        obj = User.objects.filter(username = user_name)
        if obj.count():
            raise forms.ValidationError('Tên tài khoản này đã có người sử dụng!')
        return user_name
    
    def clean_password2(self):
        data = self.cleaned_data
        if data['password2'] != data['password']:
            raise forms.ValidationError('Mật khẩu không trùng khớp!')
        return data['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        obj = User.objects.filter(email = email)
        if obj.count():
            raise forms.ValidationError('Email này đã có người sử dụng! Vui lòng sử dụng email khác')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'tri@gmail.com', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Nhập mật khẩu'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(required=False,widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'tri@ou.edu.vn', 'id': 'login-user'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control mb-3', 'placeholder': '********', 'id':'login-password'}))
    
    def __init__(self, request: Any = ..., *args: Any, **kwargs: Any) -> None:
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['password'].label = 'Mật khẩu'