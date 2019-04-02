from django.db import models
from Users.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group


class Airline(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(max_length=1500)
    image = models.ImageField()
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    airport = models.CharField(max_length=150)
    airport_code = models.CharField(max_length=10)
    lat = models.DecimalField(decimal_places=6, max_digits=15)
    lon = models.DecimalField(decimal_places=6, max_digits=15)
    image = models.ImageField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AirlineAdministrator(models.Model):
    user_profile = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user_profile.email


class AircraftModel(models.Model):
    name = models.CharField(max_length=50)
    row = models.PositiveIntegerField()
    col = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Flight(models.Model):
    destination_from = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='destination_from')
    destination_to = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='destination_to')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    #flight_time
    flight_distance = models.PositiveIntegerField()
    #flight_connnections
    aircraft_model = models.ForeignKey(AircraftModel, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)

