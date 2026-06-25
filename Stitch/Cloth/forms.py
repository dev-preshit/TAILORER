from django import forms

from Cloth.constants import GARMENT_TYPES
from .models import LowerBody, UpperBody


class UpperBodyForm(forms.ModelForm):
    
    class Meta:
        model = UpperBody
        fields = '__all__'
        widgets = {
            'clothType': forms.HiddenInput(),
        }

    def __init__(self, cloth_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clothType'].initial = cloth_type

        allowed = GARMENT_TYPES.get(cloth_type, {}).get('fields', [])
        for field in list(self.fields):
            if field not in allowed and field != 'clothType':
                del self.fields[field]




class LowerBodyForm(forms.ModelForm):
    
    class Meta:
        model = LowerBody
        fields = '__all__'
        widgets = {
            'clothType': forms.HiddenInput(),
        }

    def __init__(self, cloth_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clothType'].initial = cloth_type
        allowed = GARMENT_TYPES.get(cloth_type, {}).get('fields', [])
        for field in list(self.fields):
            if field not in allowed and field != 'clothType':  
                del self.fields[field]
