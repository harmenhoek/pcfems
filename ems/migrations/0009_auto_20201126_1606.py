# Generated by Django 3.1.3 on 2020-11-26 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0008_flag_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='qrid',
            field=models.SlugField(blank=True, max_length=10, null=True),
        ),
    ]
