# Generated by Django 2.2.1 on 2019-05-14 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FlightService', '0004_auto_20190507_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightreservation',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
