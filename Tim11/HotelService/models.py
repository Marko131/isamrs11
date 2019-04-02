from django.db import models
from Users.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(max_length=1500)
    image = models.ImageField()
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


class HotelAdministrator(models.Model):
    user_profile = models.OneToOneField(CustomUser, null=False, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel,null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_profile.email
