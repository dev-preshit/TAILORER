from django import forms

from .models import Order, OrderBottomItem, OrderTopItem
from Cloth.constants import GARMENT_TYPES

class OrderFormAddOrder(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['customer', 'days']


class OrderFormAddGarment(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['days']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     upperBody = cleaned_data.get('upperBody')
    #     lowerBody = cleaned_data.get('lowerBody')

    #     if not upperBody and not lowerBody:
    #         raise forms.ValidationError(
    #             "Pick at least one garment (upper body, lower body, or both) before saving the order."
    #         )
    #     return cleaned_data


class OrderTopItemForm(forms.ModelForm):
    
    class Meta:
        model = OrderTopItem
        fields = '__all__'


class OrderBottomItemForm(forms.ModelForm):
    
    class Meta:
        model = OrderBottomItem
        fields = '__all__'
