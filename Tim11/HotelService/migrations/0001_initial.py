# Generated by Django 2.1.7 on 2019-04-09 18:05

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
            name='Hotel',
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
            name='HotelAdministrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HotelService.Hotel')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
