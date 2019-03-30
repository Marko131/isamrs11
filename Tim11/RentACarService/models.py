from django.db import models

# Create your models here.

class RentACar(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(max_length=1500)
    image = models.ImageField()
    rating = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Rent-a-cars'


class Branch(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    rentacar = models.ForeignKey(RentACar, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Branches'
