# Generated by Django 3.1.3 on 2020-12-06 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0002_auto_20201201_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalitem',
            name='next_service_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalitem',
            name='warranty',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalitem',
            name='warranty_expiration',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='next_service_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='warranty',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='warranty_expiration',
            field=models.DateField(blank=True, null=True),
        ),
    ]
