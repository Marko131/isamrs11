from django.db import models

# Create your models here.

class Airline(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(max_length=1500)
    rating = models.FloatField()

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




