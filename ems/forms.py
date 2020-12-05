from django import forms
from .models import Item, ItemImage
from django.forms.models import inlineformset_factory


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['qrid', 'added_by', 'updated_by', 'added_on', 'last_scanned', 'status', 'location', 'user', 'date_inuse', 'date_return', ]

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        exclude = ()


# ItemImageFormSet = inlineformset_factory(
#     Item, ItemImage, form=ItemImageForm,
#     fields=['image', 'caption'], extra=3, can_delete=True
# )