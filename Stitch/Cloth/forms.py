from django import forms
from django.forms import inlineformset_factory

from Cloth.constants import GARMENT_TYPES
from .models import UpperBody, LowerBody, Options


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


UpperOptionsFormSet = inlineformset_factory(
    UpperBody,
    Options,
    fk_name='upper_body',
    fields=['text'],
    extra=1,
    can_delete=True,
)

LowerOptionsFormSet = inlineformset_factory(
    LowerBody,
    Options,
    fk_name='lower_body',
    fields=['text'],
    extra=1,
    can_delete=True,
)