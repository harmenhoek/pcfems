# Generated by Django 3.1.3 on 2021-01-18 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0013_auto_20210118_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalitem',
            name='qridcheck',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='qridcheck',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
