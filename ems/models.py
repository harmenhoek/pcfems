from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Lab(models.Model):
    number = models.CharField(max_length=5)
    manager = models.CharField(max_length=100, default='undefined')  # TODO make selectlist
    nickname = models.CharField(max_length=20, default='')

    def __str__(self):
        return f"{self.number} ({self.nickname})"

class Cabinet(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.lab.number}-{self.number}"

class Setup(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default='undefined')

    def __str__(self):
        return f"{self.lab.number} - {self.name}"

# class Location(models.Model):
#     lab = models.ForeignKey(Lab, on_delete=models.SET_NULL, null=True)
#     cabinet = models.ForeignKey(Cabinet, on_delete=models.SET_NULL, null=True, blank=True)  # how about setups?
#     setup = models.ForeignKey(Setup, on_delete=models.SET_NULL, null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.lab} - {self.cabinet}"

class Flag(models.Model):
    flag = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.flag

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):  # inherit from models, all fields below
    # General details
    # id or pk automatically created
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='uncategorized')  # TODO make selectbox
    description = models.TextField()  # longer than CharField, unrestricted text.
    purchased_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="purchaseduser")  # TODO make selectbox of users
    purchased_on = models.DateField(default="", null=True, blank=True)  # TODO not now
    purchased_price = models.DecimalField(decimal_places=2, max_digits=2, null=True, blank=True)
    storage_location = models.ForeignKey(Cabinet, on_delete=models.SET_NULL, default="", null=True, blank=True)  # TODO make different model for storage locations
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                 related_name="addeduser")  # related_name is needed since the reverse releationship (user->item, which we don't need at at all) needs a unique name. TODO make selectbox of users
    added_on = models.DateTimeField(default=timezone.now)  # TODO not now
    last_scanned = models.DateTimeField(default=timezone.now, null=True, blank=True)  # TODO link to model

    # Tracking details
    status = models.BooleanField(default=False) #false is in storage, true is in use
    location = models.ForeignKey(Setup, on_delete=models.SET_NULL, null=True) # TODO current location is now ALWAYS a setup, should also be possible to be storage
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="itemuser")
    date_inuse = models.DateField(null=True, blank=True) #TODO only show when editing item
    date_return = models.DateField(null=True, blank=True) #TODO only show when editing item

    # Editable details
    # manual = FileField
    # images = FileField
    # notes through time
    flag = models.ForeignKey(Flag, on_delete=models.SET_NULL, null=True, blank=True) #TODO only show when editing item


    def __str__(self):
        return f"{self.pk:04d} - {self.brand} {self.model} (serial: {self.serial})"







# class Logs?

# Have a timeline / log linked to each item. Different model just like Profile is to User
