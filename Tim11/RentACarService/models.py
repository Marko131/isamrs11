from django.db import models
from Users.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from datetime import datetime, timezone, date
from django.core.validators import MinValueValidator, MaxValueValidator
from FlightService.models import FlightReservation
from location_field.models.plain import PlainLocationField

class RentACar(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(max_length=1500)
    image = models.ImageField()
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Rent-a-cars'


class Branch(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    rentacar = models.ForeignKey(RentACar, on_delete=models.CASCADE)
    location = PlainLocationField(based_fields=['city'], zoom=7, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Branches'


class Vehicle(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    manufacturer = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(default=1)
    rentacar = models.ForeignKey(RentACar, on_delete=models.CASCADE)
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)])
    image = models.ImageField(blank=True, null=True)

    @property
    def price_with_discount(self):
        return float(self.price * (100 - self.discount)) / 100.00

    def __str__(self):
        return self.manufacturer + " " + self.model_name


class RentACarAdministrator(models.Model):
    user_profile = models.OneToOneField(CustomUser, null=False, on_delete=models.CASCADE)
    rentacarservice = models.ForeignKey(RentACar, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_profile.email


@receiver(post_save, sender=RentACarAdministrator)
def assign_group(sender, instance, created, **kwargs):
    group = Group.objects.get(name='RentACarAdministrator')
    group.user_set.add(instance.user_profile)


class VehicleReservation(models.Model):
    flight_reservation = models.ForeignKey(FlightReservation, on_delete=models.CASCADE, null=True, blank=True)
    quick = models.BooleanField(default=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True, blank=True)
    reserved_from = models.DateField()
    reserved_to = models.DateField()

    def __str__(self):
        return str(self.pk) + " " + str(self.vehicle) + " " + str(self.user)

    @property
    def is_past(self):
        return date.today() > self.reserved_to

    def get_rate(self):
        vehicle_rate = VehicleRating.objects.get(user=self.user, vehicle=self.vehicle)
        if vehicle_rate:
            return vehicle_rate.rate
        return 0


class VehicleRating(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)
