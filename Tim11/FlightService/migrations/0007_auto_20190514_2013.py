# Generated by Django 2.2.1 on 2019-05-14 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FlightService', '0006_flightreservation_passport'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightreservation',
            name='creator',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='flightreservation',
            name='quick',
            field=models.BooleanField(default=False),
        ),
    ]
