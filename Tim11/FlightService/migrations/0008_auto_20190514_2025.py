# Generated by Django 2.2.1 on 2019-05-14 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FlightService', '0007_auto_20190514_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightreservation',
            name='passport',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
