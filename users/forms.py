from django import forms
from django.contrib.auth.models import User # imports the User data
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
   email = forms.EmailField() # default=True by default

   class Meta:  # specify model it will interact with
       model = User
       fields = ['username', 'email', 'password1', 'password2']  # fields to show in form and the order

class ProfileUpdateForm(forms.ModelForm):
   class Meta:
       model = Profile
       fields = ['image']
