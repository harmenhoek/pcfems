from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy  # for redirect after adding item
from PIL import Image
import os
import time
from simple_history.models import HistoricalRecords
from simple_history import register
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

register(User)  # to allow simple_history to track it

# set __str__ for user
def get_first_name(self):
    return f'{self.first_name} {self.last_name}'

User.add_to_class("__str__", get_first_name)

class Lab(models.Model):
    number = models.CharField(max_length=5)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=2, limit_choices_to={'is_superuser': False})
    nickname = models.CharField(max_length=20, default='', null=True, blank=True)
    image = models.ImageField(upload_to='lab_pics', blank=True, null=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # initial save (incl image)
        if self.image:
            instance = super(Lab, self).save(*args, **kwargs)
            image = Image.open(self.image.path)
            image.save(self.image.path, quality=15, optimize=True)
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} ({self.nickname})"

class Cabinet(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    nickname = models.CharField(max_length=25, blank=True, null=True)
    main_content = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, help_text="Cabinet owner is person whose stuff is stored in it.")
    image = models.ImageField(upload_to='cabinet_pics', blank=True, null=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # initial save (incl image)
        if self.image:
            instance = super(Lab, self).save(*args, **kwargs)
            image = Image.open(self.image.path)
            image.save(self.image.path, quality=15, optimize=True)
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lab.number} - {self.number}"

class Setup(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default='undefined', limit_choices_to={'is_superuser': False})
    image = models.ImageField(upload_to='setup_pics', blank=True, null=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # initial save (incl image)
        if self.image:
            instance = super(Lab, self).save(*args, **kwargs)
            image = Image.open(self.image.path)
            image.save(self.image.path, quality=15, optimize=True)
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lab.number} - {self.name}"

class Flag(models.Model):
    flag = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, default='bug', help_text='Set a icon from <a target="_blank" href="https://fontawesome.com/icons?m=free">this library</a>.')
    history = HistoricalRecords()

    def __str__(self):
        return self.flag

class Category(models.Model):
    name = models.CharField(max_length=100, help_text='Please verify that no such category already exists.')
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Item(models.Model):  # inherit from models, all fields below
    # General details
    # id or pk automatically created
    qrid = models.SlugField(max_length=10, null=True, blank=True)
    version = models.IntegerField(null=True, blank=True, default=1)
    labelstatus = models.DateTimeField(default=None, null=True, blank=True)

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100, help_text="If multiple parts (e.g. proprietary power supply) with multiple models, comma separate models.")
    title = models.CharField(max_length=25, help_text="Add short title that describes the item. E.g. 'Multimeter 0-1000V'.")
    serial = models.CharField(max_length=100, null=True, blank=True, help_text="Comma separate multiple serial numbers.")
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='', blank=True, help_text='New categories can be added in Admin/Manage/Categories.')
    description = models.TextField(help_text="Add as many terms printed on the item and possible search terms.")  # longer than CharField, unrestricted text.
    purchased_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchaseduser", limit_choices_to={'is_superuser': False})
    purchased_on = models.DateField(default="", null=True, blank=True)
    purchased_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    warranty = models.BooleanField(default=False)
    warranty_expiration = models.DateField(null=True, blank=True)
    next_service_date = models.DateField(null=True, blank=True)
    storage_location = models.ForeignKey(Cabinet, on_delete=models.SET_NULL, default="", null=True, blank=True, help_text='New storage locations can be added in Admin/Manage/Locations.')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 related_name="addeduser", limit_choices_to={'is_superuser': False})  # related_name is needed since the reverse releationship (user->item, which we don't need at at all) needs a unique name.
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 related_name="updateduser", limit_choices_to={'is_superuser': False})
    added_on = models.DateTimeField(default=timezone.now)
    last_scanned = models.DateTimeField(default=timezone.now, null=True, blank=True)  # TODO link to model and add to history.

    #.objects.all().exclude(is_superuser=True)

    # Tracking details
    tracking = models.BooleanField(default=True, help_text="Tracking allows for assigning an item to a user and location, common items such as multimeters are not tracked.")
    status = models.BooleanField(default=True) #True is in storage (item is free), False is in use (assigned to)
    location = models.ForeignKey(Setup, on_delete=models.SET_NULL, null=True)
    parts = models.IntegerField(default=1, help_text="Number of separate parts, e.g. when an item has a proprietary power supply.")
    # location = ForeignKey(Setup OR Cabinet)

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # location2 = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="itemuser", limit_choices_to={'is_superuser': False}, help_text="Optional, only the location is mandatory.")
    date_inuse = models.DateField(null=True, blank=True)
    date_return = models.DateField(null=True, blank=True, help_text="Optional, but recommended.")

    # Editable details
    # manual = FileField
    # images = FileField
    # notes through time
    flag = models.ForeignKey(Flag, on_delete=models.SET_NULL, null=True, blank=True)
    flag_comment = models.CharField(max_length=100, null=True, blank=True)
    # flagged_by = models.ForeignKey(User, default=2, on_delete=models.SET_NULL, null=True, blank=True, related_name="flaggedbyuser")
    image = models.ImageField(default='default.png', upload_to='item_pics', blank=True, null=True)
    image2 = models.ImageField(upload_to='item_pics', blank=True, null=True)
    history = HistoricalRecords() # excluded_fields=['pub_date']


    def __str__(self):
        return f"{self.pk:04d} - {self.brand} {self.model} (serial: {self.serial})"

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # initial save (incl image)
        if self.qrid == '' or self.qrid is None:
            self.qrid = f"PCF{self.pk:04d}"
            super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            maxsize = 1000
            if img.height > maxsize or img.width > maxsize:  # TODO move this to views?!
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
        else:
            self.image = 'default.png'
            super().save(*args, **kwargs)


class ItemImage(models.Model): # currently not in use
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.RESTRICT, limit_choices_to={'is_superuser': False})
    added_on = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='item_pics')
    caption = models.CharField(max_length=200, blank=True, null=True)
    history = HistoricalRecords()

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # image = GenericForeignKey('content_type', 'object_id')


    def __str__(self):
        return f"{self.item.pk} - {self.image.name}"

class ItemLog(models.Model):
    item = models.ForeignKey(Item, related_name='logs', on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.RESTRICT, limit_choices_to={'is_superuser': False})
    added_on = models.DateTimeField(default=timezone.now)
    log = models.TextField()
    file1 = models.FileField(blank=True, null=True)
    file1_name = models.CharField(max_length=20, null=True, blank=True)
    file2 = models.FileField(blank=True, null=True)
    file2_name = models.CharField(max_length=20, null=True, blank=True)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse_lazy('item-detail', args=[str(self.item.pk)])

    def __str__(self):
        return f"{self.item.pk} - {self.added_on} - {self.added_by}"

    def file1_extension(self):
        name, extension = os.path.splitext(self.file1.name)
        return extension

    def file2_extension(self):
        name, extension = os.path.splitext(self.file2.name)
        return extension