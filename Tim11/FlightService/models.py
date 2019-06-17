from builtins import set
from django.db import models
from Users.models import CustomUser
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from datetime import datetime, timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from location_field.models.plain import PlainLocationField
from django.utils import datetime_safe

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
    image = models.ImageField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    location = PlainLocationField(based_fields=['city'], zoom=7, null=True)

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
    flight_distance = models.PositiveIntegerField()
    connections = models.CharField(max_length=500, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    rows_economy = models.PositiveIntegerField(default=0)
    cols_economy = models.PositiveIntegerField(default=0)
    rows_business = models.PositiveIntegerField(default=0)
    cols_business = models.PositiveIntegerField(default=0)
    rows_first = models.PositiveIntegerField(default=0)
    cols_first = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(99)])
    checked_baggage = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    @property
    def price_with_discount(self):
        return float(self.price * (100 - self.discount)) / 100.00

    @property
    def get_average_rate(self):
        ratings = [rating.rate for rating in FlightRating.objects.filter(flight=self)]
        if ratings:
            return float(sum(ratings)) / len(ratings)
        return 0
    
    @property
    def available_class(self):
        cl = []
        if self.rows_economy and self.cols_economy:
            cl.append("Economy")
        if self.rows_business and self.cols_business:
            cl.append("Business")
        if self.rows_first and self.cols_first:
            cl.append("First")
        return cl

    @property
    def seats_count(self):
        return self.seat_set.count()

    def __str__(self):
        return f'{self.pk} - {self.destination_from} - {self.destination_to}'


class Seat(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, default=None)
    available = models.BooleanField(default=True)
    row = models.PositiveIntegerField()
    col = models.PositiveIntegerField()
    type = models.CharField(max_length=10, default="")

    def __str__(self):
        return f'Flight {self.flight.id} - {self.type} {self.row} {self.col}'

    @property
    def rowcol(self):
        return f'{self.type} {self.row} - {self.col}'


@receiver(post_save, sender=Flight)
def create_seats(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.rows_economy > 0 and instance.cols_economy:
        for i in range(instance.rows_economy):
            for j in range(instance.cols_economy):
                Seat.objects.create(flight=instance, row=i+1, col=j+1, type="Economy")
    if instance.rows_business > 0 and instance.cols_business:
        for i in range(instance.rows_business):
            for j in range(instance.cols_business):
                Seat.objects.create(flight=instance, row=i+1, col=j+1, type="Business")
    if instance.rows_first > 0 and instance.cols_first:
        for i in range(instance.rows_first):
            for j in range(instance.cols_first):
                Seat.objects.create(flight=instance, row=i+1, col=j+1, type="First")


class FlightReservation(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True, blank=True)
    accepted = models.BooleanField(default=False)
    passport = models.CharField(max_length=20, default='', null=True, blank=True)
    quick = models.BooleanField(default=False)
    creator = models.BooleanField(default=True)
    date_created = models.DateField(null=True)

    def __str__(self):
        return str(self.pk) + str(self.seat)

    @property
    def is_past(self):
        return datetime.now() > self.seat.flight.arrival_time

    def get_rate(self):
        flight_rate = FlightRating.objects.get(user=self.user, flight=self.seat.flight)
        if flight_rate:
            return flight_rate.rate
        return 0

    def delete(self, using=None, keep_parents=False):
        self.seat.available = True
        self.seat.save()
        super(FlightReservation, self).delete()


@receiver(post_save, sender=FlightReservation)
def take_seat(sender, instance, created, **kwargs):
    seat = get_object_or_404(Seat, pk=instance.seat.pk)
    seat.available = False
    seat.save()


class FlightRating(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)

