from django.contrib import admin
from .models import Destination, Airline, AirlineAdministrator, AircraftModel, Flight

from django.contrib.auth.models import User

class AirlineAdministratorInline(admin.TabularInline):
    model = AirlineAdministrator
    extra = 0


class AirlineAdmin(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ('rating',)
    readonly_fields = ('rating', )
    inlines = [AirlineAdministratorInline]

    def get_queryset(self, request):
        qs = super(AirlineAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(airlineadministrator__user_profile=request.user)


class DestinationAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(DestinationAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['airline'].queryset = Airline.objects.filter(airlineadministrator__user_profile=request.user)
        else:
            form.base_fields['airline'].queryset = Airline.objects.all()
        return form

    def get_queryset(self, request):
        qs = super(DestinationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(airline=request.user.airlineadministrator.airline)


class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'destination_from', 'destination_to', 'departure_time', 'arrival_time')

    def get_queryset(self, request):
        qs = super(FlightAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(airline=request.user.airlineadministrator.airline)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(FlightAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['airline'].queryset = Airline.objects.filter(airlineadministrator__airline=request.user.airlineadministrator.airline)
        else:
            form.base_fields['airline'].queryset = Airline.objects.all()
        return form

admin.site.register(AirlineAdministrator)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Airline, AirlineAdmin)
admin.site.register(AircraftModel)
admin.site.register(Flight, FlightAdmin)


