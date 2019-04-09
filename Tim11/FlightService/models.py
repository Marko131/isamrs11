from django.db import models
from Users.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class Flight(models.Model):
    destination_from = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='destination_from')
    destination_to = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='destination_to')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    #flight_time
    flight_distance = models.PositiveIntegerField()
    #flight_connnections
    price = models.DecimalField(decimal_places=2, max_digits=10)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    row = models.PositiveIntegerField(default=1)
    col = models.PositiveIntegerField(default=1)


class Seat(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, default=None)
    available = models.BooleanField(default=True)
    row = models.PositiveIntegerField()
    col = models.PositiveIntegerField()

    def __str__(self):
        return f'Flight {self.flight.id} - {self.row} {self.col}'


@receiver(post_save, sender=Flight)
def create_seats(sender, instance, created, **kwargs):
    if created:
        for i in range(instance.row):
            for j in range(instance.col):
                Seat.objects.create(flight=instance, row=i+1, col=j+1)