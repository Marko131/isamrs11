# Generated by Django 2.2 on 2019-04-09 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HotelService', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('capacity', models.PositiveIntegerField(default=1)),
                ('floor', models.PositiveIntegerField(default=1)),
                ('balcony', models.BooleanField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HotelService.Hotel')),
            ],
        ),
    ]