from django import forms
from django.contrib.auth.models import User  # imports the User data
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Preferences


class UserRegisterForm(UserCreationForm):
   email = forms.EmailField()  # default=True by default

   class Meta:  # specify model it will interact with
       model = User
       fields = ['username', 'email', 'password1', 'password2']  # fields to show in form and the order

class ProfileUpdateForm(forms.ModelForm):
   class Meta:
       model = Profile
       fields = ['image']

class ManageUserUpdateForm(forms.ModelForm):
    # extra fields
    is_admin = forms.BooleanField(required=False, label="System administator", help_text='Can do everything, including changing system settings.')
    is_itemmoderator = forms.BooleanField(required=False, label="Item moderator", help_text='Can add and modify equipment.')
    is_usermoderator = forms.BooleanField(required=False, label="User moderator", help_text='Can add and modify users.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active']

class SettingUpdateForm(forms.ModelForm):
    class Meta:
        model = Preferences
        exclude = ('user', )