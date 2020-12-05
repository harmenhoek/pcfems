from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from django.contrib.auth.models import AbstractUser
from activity_log.models import UserMixin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  #one-to-one relationship: one profile per user, one user per profile
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



# # Only for LAST_ACTIVITY = True
# class User(AbstractUser, UserMixin):
#     pass