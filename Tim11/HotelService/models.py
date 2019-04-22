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


class Room(models.Model):
    type = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=1)
    floor = models.PositiveIntegerField(default=1)
    balcony = models.BooleanField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    hotel = models.ForeignKey(Hotel, null=False, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.pk) + " " + self.type


class HotelAdministrator(models.Model):
    user_profile = models.OneToOneField(CustomUser, null=False, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel,null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_profile.email

@receiver(post_save, sender=HotelAdministrator)
def assign_group(sender, instance, created, **kwargs):
    group = Group.objects.get(name='HotelAdministrator')
    group.user_set.add(instance.user_profile)
