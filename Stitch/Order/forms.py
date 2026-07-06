from django import forms

from .models import Order
from Cloth.constants import GARMENT_TYPES

class OrderFormAddOrder(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['customer', 'days']


class OrderFormAddGarment(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['customer', 'upperBody', 'lowerBody', 'status', 'days']


