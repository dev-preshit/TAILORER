from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class UserRegisterForm(UserCreationForm):
    phone_no = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1', 'password2']


class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ['name', 'phone']

