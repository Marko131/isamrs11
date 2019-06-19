# Generated by Django 2.2.1 on 2019-06-19 21:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FlightService', '0008_auto_20190616_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='discount',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)]),
        ),
    ]
