from django import forms

from .models import Order
from Cloth.constants import GARMENT_TYPES

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = '__all__'

