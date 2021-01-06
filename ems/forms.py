from django import forms
from .models import Item, ItemImage
from django.forms.models import inlineformset_factory
from bootstrap_datepicker_plus import DatePickerInput

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['qrid', 'added_by', 'updated_by', 'added_on', 'last_scanned', 'status', 'location', 'user', 'date_inuse', 'date_return', 'flag']
        widgets = {
            'purchased_on': DatePickerInput(format='%Y-%m-%d'),
            'warranty_expiration': DatePickerInput(format='%Y-%m-%d'),
            'next_service_date': DatePickerInput(format='%Y-%m-%d'),
        }

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        exclude = ()


# ItemImageFormSet = inlineformset_factory(
#     Item, ItemImage, form=ItemImageForm,
#     fields=['image', 'caption'], extra=3, can_delete=True
# )