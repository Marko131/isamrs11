# Generated by Django 2.2.1 on 2019-06-14 17:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FlightService', '0004_flight_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='checked_baggage',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='flight',
            name='discount',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(99)]),
        ),
        migrations.AlterField(
            model_name='flightreservation',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='FlightService.Seat'),
        ),
    ]
