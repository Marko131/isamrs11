from django.contrib import admin
from .models import Destination, Airline
# Register your models here.

class AirlineAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Destination)
admin.site.register(Airline, AirlineAdmin)
