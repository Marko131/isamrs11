# Generated by Django 2.1.7 on 2019-03-26 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=1500)),
                ('image', models.ImageField(upload_to='')),
                ('rating', models.FloatField()),
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
    ]
