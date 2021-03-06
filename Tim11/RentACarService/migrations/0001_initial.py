# Generated by Django 2.1.7 on 2019-05-20 15:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='RentACar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=1500)),
                ('image', models.ImageField(upload_to='')),
                ('rating', models.FloatField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Rent-a-cars',
            },
        ),
        migrations.CreateModel(
            name='RentACarAdministrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rentacarservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentACarService.RentACar')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('manufacturer', models.CharField(max_length=100)),
                ('model_name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('rentacar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentACarService.RentACar')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentACarService.Vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserved_from', models.DateTimeField()),
                ('reserved_to', models.DateTimeField()),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentACarService.Vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='rentacar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentACarService.RentACar'),
        ),
    ]
