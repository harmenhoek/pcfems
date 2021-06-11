from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  #one-to-one relationship: one profile per user, one user per profile
    image = models.ImageField(default='default.png', upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            width, height = img.size
            output_size = (min(width, height), min(width, height))
            left = (width - output_size[0]) / 2
            top = (height - output_size[1]) / 2
            right = (width + output_size[0]) / 2
            bottom = (height + output_size[1]) / 2
            img = img.crop((left, top, right, bottom))
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)  # TODO include newer image processing from ems/models

    class Meta:
        permissions = (
            ("is_itemmoderator", "Can add and modify items"),
            ("is_usermoderator", "Can add and modify users"),
            ("is_admin", "Is system administrator"),
        )

class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    help_on = models.BooleanField(default=1, help_text="Show help buttons through the application when available.")
    home_itemsshown = models.IntegerField(default=10)  # TODO: make this a ChoiceField like in ems_manage/forms.

    # update_message = models.BooleanField(default=1)  # show post-update message to all users

    def __str__(self):
        return str(self.user)+'s' + 'preferences'