# Generated by Django 2.1.7 on 2019-04-02 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_customuser_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
    ]
