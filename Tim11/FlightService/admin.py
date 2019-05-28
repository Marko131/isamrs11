from django.contrib import admin
from .models import Destination, Airline, AirlineAdministrator, Flight, Seat, FlightReservation, FlightRating
from Users.models import CustomUser
from django.contrib.auth.models import Group


class AirlineAdministratorInline(admin.TabularInline):
    model = AirlineAdministrator
    extra = 0

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0

class AircraftModelAdmin(admin.ModelAdmin):
    inlines = [SeatInline]

class AirlineAdmin(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ('rating',)
    #readonly_fields = ('rating', )
    inlines = [AirlineAdministratorInline]

    def get_queryset(self, request):
        qs = super(AirlineAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(airlineadministrator__user_profile=request.user)


class DestinationAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['airline']
        else:
            return []

    def get_queryset(self, request):
        qs = super(DestinationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(airline=request.user.airlineadministrator.airline)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.airline = request.user.airlineadministrator.airline
        super().save_model(request, obj, form, change)


class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'destination_from', 'destination_to', 'departure_time', 'arrival_time')

    def get_queryset(self, request):
        qs = super(FlightAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(airline=request.user.airlineadministrator.airline)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['airline']
        else:
            return []

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.airline = request.user.airlineadministrator.airline
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(FlightAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        form.base_fields['destination_from'].queryset = Destination.objects.filter(airline=request.user.airlineadministrator.airline)
        form.base_fields['destination_to'].queryset = Destination.objects.filter(airline=request.user.airlineadministrator.airline)
        return form


class AirlineAdministratorAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(AirlineAdministratorAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user_profile'].queryset = CustomUser.objects.filter(is_staff=True, groups__isnull=True, is_superuser=False)
        return form


class SeatAdmin(admin.ModelAdmin):
    readonly_fields = ['flight', 'row', 'col', 'available']

    def get_queryset(self, request):
        qs = super(SeatAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(flight__airline=request.user.airlineadministrator.airline)


class FlightReservationAdmin(admin.ModelAdmin):
    readonly_fields = ['user']

    def get_queryset(self, request):
        qs = super(FlightReservationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(seat__flight__airline=request.user.airlineadministrator.airline)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(FlightReservationAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            form.base_fields['seat'].queryset = Seat.objects.filter(available=True)
            return form
        form.base_fields['seat'].queryset = Seat.objects.filter(flight__airline=request.user.airlineadministrator.airline, available=True)
        return form

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()




admin.site.register(AirlineAdministrator, AirlineAdministratorAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Airline, AirlineAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(FlightReservation, FlightReservationAdmin)
admin.site.register(FlightRating)
