# Generated by Django 2.1.7 on 2019-04-02 14:54

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
                ('rating', models.FloatField()),
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
        migrations.AddField(
            model_name='branch',
            name='rentacar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RentACarService.RentACar'),
        ),
    ]
