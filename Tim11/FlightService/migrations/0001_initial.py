# Generated by Django 2.1.7 on 2019-03-30 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AircraftModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('row', models.PositiveIntegerField()),
                ('col', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=1500)),
                ('image', models.ImageField(upload_to='')),
                ('rating', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AirlineAdministrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airline', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FlightService.Airline')),
                ('user_profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
                ('airport', models.CharField(max_length=150)),
                ('airport_code', models.CharField(max_length=10)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=15)),
                ('lon', models.DecimalField(decimal_places=6, max_digits=15)),
                ('image', models.ImageField(upload_to='')),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlightService.Airline')),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('flight_distance', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('aircraft_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlightService.AircraftModel')),
                ('airline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlightService.Airline')),
                ('destination_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_from', to='FlightService.Destination')),
                ('destination_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_to', to='FlightService.Destination')),
            ],
        ),
    ]
