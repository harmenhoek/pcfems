# Generated by Django 3.1.3 on 2020-11-23 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setup',
            name='lab',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ems.lab'),
            preserve_default=False,
        ),
    ]
