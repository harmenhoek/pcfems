from django import forms

choices = [(True, 'Items with "Tracking"'),
           (False, 'Items with "No Tracking"')]

class ExportForm(forms.Form):
    pk1 = forms.IntegerField(label='Start ID')
    pk2 = forms.IntegerField(label='End ID')
    tracking = forms.ChoiceField(choices=choices, widget=forms.RadioSelect(), help_text='Tracked items require a different label template than non-tracked items. Export separately and use print labels separately.')

class SettingsForm(forms.Form):
    pass
# TODO add model here.