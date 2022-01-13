from django.db import models
from django.urls import reverse, reverse_lazy
from simple_history.models import HistoricalRecords
from simple_history import register
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# from dynamic_preferences.registries import global_preferences_registry
# global_preferences = global_preferences_registry.manager()

class Ofi(models.Model):
    number = models.PositiveIntegerField(validators=[MinValueValidator(10_000_000), MaxValueValidator(99_999_999)])
    name = models.CharField(max_length=50, help_text="Easy to remember name")
    description = models.TextField()
    project = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.number} - {self.name}"

class OrderCategory(models.Model):
    name = models.CharField(max_length=30)
    orderer = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null=True, related_name='order_orderer', help_text="")
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = [
        (1, 'Requested'),
        (2, 'Approved'),
        (3, 'Ordered'),
        (4, 'Not approved'),
        (5, 'Finished'),
        (6, 'Canceled')
    ]
    name = models.CharField(max_length=30, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_person', help_text="")
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    ofi = models.ForeignKey(Ofi, on_delete=models.RESTRICT)
    url = models.URLField(null=True, blank=True)
    notes = models.TextField(help_text="")
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_approver', help_text="")

    status = models.PositiveSmallIntegerField(choices=STATUS, default=1)
    category = models.ForeignKey(OrderCategory, on_delete=models.PROTECT)
    added_by = models.ForeignKey(User, on_delete=models.RESTRICT, limit_choices_to={'is_superuser': False})
    added_on = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.pk} - {self.name} (for: {self.user})"


class OrderLog(models.Model):
    order = models.ForeignKey(Order, related_name='order_logs', on_delete=models.CASCADE)
    comment = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.RESTRICT, limit_choices_to={'is_superuser': False})
    added_on = models.DateTimeField(default=timezone.now)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.order.pk} - {self.added_on}"
