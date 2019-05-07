from django.db import models
from Users.models import CustomUser
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from datetime import datetime, timezone
from django.core.validators import MinValueValidator, MaxValueValidator

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


@receiver(post_save, sender=AirlineAdministrator)
def assign_group(sender, instance, created, **kwargs):
    group = Group.objects.get(name='AirlineAdministrator')
    group.user_set.add(instance.user_profile)


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
    rows_economy = models.PositiveIntegerField(default=0)
    cols_economy = models.PositiveIntegerField(default=0)
    rows_business = models.PositiveIntegerField(default=0)
    cols_business = models.PositiveIntegerField(default=0)
    rows_first = models.PositiveIntegerField(default=0)
    cols_first = models.PositiveIntegerField(default=0)


class Seat(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, default=None)
    available = models.BooleanField(default=True)
    row = models.PositiveIntegerField()
    col = models.PositiveIntegerField()
    type = models.CharField(max_length=10, default="")

    def __str__(self):
        return f'Flight {self.flight.id} - {self.type} {self.row} {self.col}'


@receiver(post_save, sender=Flight)
def create_seats(sender, instance, created, **kwargs):
    if created:
        for i in range(instance.rows_economy):
            for j in range(instance.cols_economy):
                Seat.objects.create(flight=instance, row=i+1, col=j+1, type="Economy")
        for i in range(instance.rows_business):
            for j in range(instance.cols_business):
                Seat.objects.create(flight=instance, row=i+1, col=j+1, type="Business")
        for i in range(instance.rows_first):
            for j in range(instance.cols_first):
                Seat.objects.create(flight=instance, row=i+1, col=j+1, type="First")


class FlightReservation(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return str(self.pk) + str(self.seat)

    @property
    def is_past(self):
        return datetime.now(timezone.utc) > self.seat.flight.arrival_time

    def get_rate(self):
        flight_rate = FlightRating.objects.get(user=self.user, flight=self.seat.flight)
        if flight_rate:
            return flight_rate.rate
        return 0


@receiver(post_save, sender=FlightReservation)
def take_seat(sender, instance, created, **kwargs):
    seat = get_object_or_404(Seat, pk=instance.seat.pk)
    seat.available = False
    seat.save()


class FlightRating(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)

