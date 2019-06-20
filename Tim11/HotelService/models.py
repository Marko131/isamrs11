from django.db import models
from Users.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from FlightService.models import FlightReservation
from datetime import date, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from location_field.models.plain import PlainLocationField

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=1500)
    image = models.ImageField()
    rating = models.FloatField(default=0)
    airport_transfer = models.BooleanField(default=False)
    airport_transfer_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    parking = models.BooleanField(default=False)
    parking_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    pool = models.BooleanField(default=False)
    pool_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    restaurant = models.BooleanField(default=False)
    restaurant_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    gym = models.BooleanField(default=False)
    gym_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    spa = models.BooleanField(default=False)
    spa_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    room_service = models.BooleanField(default=False)
    room_service_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    wifi = models.BooleanField(default=False)
    wifi_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    location = PlainLocationField(based_fields=['city'], zoom=7, null=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    type = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=1)
    floor = models.PositiveIntegerField(default=1)
    balcony = models.BooleanField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    hotel = models.ForeignKey(Hotel, null=False, on_delete=models.CASCADE)
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)])
    image = models.ImageField(blank=True, null=True)

    @property
    def price_with_discount(self):
        return float(self.price * (100 - self.discount)) / 100.00

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


class HotelReservation(models.Model):
    flight_reservation = models.ForeignKey(FlightReservation, on_delete=models.CASCADE, null=True, blank=True)
    quick = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True, blank=True)
    reserved_from = models.DateField()
    reserved_to = models.DateField()

    @property
    def is_past(self):
        return date.today() > self.reserved_to

    def get_rate(self):
        room_rate = RoomRating.objects.get(user=self.user, room=self.room)
        if room_rate:
            return room_rate.rate
        return 0


class RoomRating(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)