from django import forms
from .models import Item, ItemImage, Category
from django.forms.models import inlineformset_factory
from bootstrap_datepicker_plus import DatePickerInput

class ItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(  # to set the initial value to blank, but still require it. Makes user actively select value.
        queryset=Category.objects.all(),
        required=True
    )

    class Meta:
        model = Item
        fields = ['title', 'category', 'brand', 'model', 'serial', 'parts', 'description', 'storage_location', 'image', 'image2',
                  'purchased_by', 'purchased_on', 'purchased_price', 'warranty', 'warranty_expiration', 'next_service_date']
        # exclude = ['qrid', 'added_by', 'updated_by', 'added_on', 'last_scanned', 'status', 'location', 'user',
        #            'date_inuse', 'date_return', 'flag', 'flag_comment', 'labelstatus', 'version']
        widgets = {
            'purchased_on': DatePickerInput(format='%Y-%m-%d'),
            'warranty_expiration': DatePickerInput(format='%Y-%m-%d'),
            'next_service_date': DatePickerInput(format='%Y-%m-%d'),
        }

class AssignForm(forms.ModelForm):  # added to include date selector widget
    class Meta:
        model = Item
        fields = ['location', 'user', 'date_return']
        widgets = {
            'date_return': DatePickerInput(format='%Y-%m-%d'),
        }

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        exclude = ()


# ItemImageFormSet = inlineformset_factory(
#     Item, ItemImage, form=ItemImageForm,
#     fields=['image', 'caption'], extra=3, can_delete=True
# )