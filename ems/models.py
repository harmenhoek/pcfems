from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse # for redirect after adding item
from PIL import Image
import os
import time
from simple_history.models import HistoricalRecords
from simple_history import register

register(User) # to allow simple_history to track it

# set __str__ for user
def get_first_name(self):
    return f'{self.first_name} {self.last_name}'

User.add_to_class("__str__", get_first_name)

class Lab(models.Model):
    number = models.CharField(max_length=5)
    manager = models.CharField(max_length=100, default='undefined')  # TODO make selectlist
    nickname = models.CharField(max_length=20, default='')
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.number} ({self.nickname})"

class Cabinet(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.lab.number}-{self.number}"

class Setup(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default='undefined', limit_choices_to={'is_superuser': False})
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.lab.number} - {self.name}"

class Flag(models.Model):
    flag = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, default='bug')
    history = HistoricalRecords()

    def __str__(self):
        return self.flag

class Category(models.Model):
    name = models.CharField(max_length=100)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Item(models.Model):  # inherit from models, all fields below
    # General details
    # id or pk automatically created
    qrid = models.SlugField(max_length=10, null=True, blank=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='uncategorized')  # TODO make selectbox
    description = models.TextField()  # longer than CharField, unrestricted text.
    purchased_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchaseduser", limit_choices_to={'is_superuser': False})  # TODO make selectbox of users
    purchased_on = models.DateField(default="", null=True, blank=True)  # TODO not now
    purchased_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    # warranty_expiration = models.DateField(null=True, blank=True)
    # next_service_date = models.DateField(null=True, blank=True)
    storage_location = models.ForeignKey(Cabinet, on_delete=models.SET_NULL, default="", null=True, blank=True)  # TODO make different model for storage locations
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 related_name="addeduser", limit_choices_to={'is_superuser': False})  # related_name is needed since the reverse releationship (user->item, which we don't need at at all) needs a unique name. TODO make selectbox of users
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 related_name="updateduser", limit_choices_to={'is_superuser': False})
    added_on = models.DateTimeField(default=timezone.now)
    last_scanned = models.DateTimeField(default=timezone.now, null=True, blank=True)  # TODO link to model

#.objects.all().exclude(is_superuser=True)

    # Tracking details
    status = models.BooleanField(default=False) #false is in storage, true is in use
    location = models.ForeignKey(Setup, on_delete=models.SET_NULL, null=True) # TODO current location is now ALWAYS a setup, should also be possible to be storage
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="itemuser", limit_choices_to={'is_superuser': False})
    date_inuse = models.DateField(null=True, blank=True) #TODO only show when editing item
    date_return = models.DateField(null=True, blank=True) #TODO only show when editing item

    # Editable details
    # manual = FileField
    # images = FileField
    # notes through time
    flag = models.ForeignKey(Flag, on_delete=models.SET_NULL, null=True, blank=True) #TODO only show when editing item
    image = models.ImageField(default='default.png', upload_to='item_pics')
    history = HistoricalRecords()


    def __str__(self):
        return f"{self.pk:04d} - {self.brand} {self.model} (serial: {self.serial})"

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # initial save (incl image)
        if self.qrid == '':
            self.qrid = f"PCF{self.pk:04d}"
            super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        maxsize = 1000
        if img.height > maxsize or img.width > maxsize:
            output_size = (maxsize, maxsize)
            img.thumbnail(output_size)
            # rename (TODO what if user uploads small image? Now no rename)
            path = os.path.dirname(self.image.path)
            ext = os.path.splitext(self.image.path)[1]
            shorthash = hash(time.time())
            file_new = os.path.join(path, str(self.pk) + '_' + str(shorthash) + ext)
            img.save(file_new)
            os.remove(self.image.path)
            file_new_short: str = os.path.join('item_pics/', str(self.pk) + '_' + str(shorthash) + ext)
            self.image = file_new_short
            super().save(*args, **kwargs)


# class Logs?

# Have a timeline / log linked to each item. Different model just like Profile is to User
